from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from wedsite.rsvp.models import Guest, Event, Person, Rsvp, Interest
from django.template import RequestContext
from django.middleware.csrf import CsrfViewMiddleware
from django.utils.translation import ugettext as _
import requests

from django.contrib.auth import get_user_model, authenticate, login, logout
User = get_user_model()

import requests
import environ

from .forms import CodeForm, RequestForm, SoonForm, EventForm, PostRsvpForm

env = environ.Env()

from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = { message_constants.ERROR: 'danger',}

def interest(request, guest_id, event_id):
	guest = Guest.objects.get(email=guest_id)
	event = Event.objects.get(pk=event_id)
	count = Interest.objects.filter(event__id=event_id, guest__email=guest_id).count()
	if (count == 0):
		newInterested = Interest(event=event, guest=guest)
		newInterested.save()
	context = RequestContext(request, {
		'guest' : guest,
		'event' : event,
		})
	return render_to_response('rsvp/interest.html', context_instance = context)

def soon(request):
	if request.method == 'POST':
		form = SoonForm(request.POST)
		if form.is_valid():
			email = request.POST.get("email", "")
			response = add_to_rsvp_mailing_list(email)
			print(response.json)
			messages.add_message(request, messages.SUCCESS, _("We'll let you know when RSVP is open. Thanks!"))
			return render(request, 'rsvp/soon.html', {'form': form})
		else:
			messages.add_message(request, messages.ERROR, _('There were problems with your request.'))
			return render(request, 'rsvp/soon.html', {'form': form})

	else:
		form = SoonForm()
		return render(request, 'rsvp/soon.html', {'form': form})


def create_initial_form(guest, all_on=False):
	initial = {}
	people = guest.person_set.all()
	wedding = Event.objects.get(pk=1)
	for person in people:
		if all_on:
			initial[person.name] = 'on'
		else:
			try:
				rsvp = Rsvp.objects.get(person=person, event=wedding)
			except Rsvp.DoesNotExist:
				rsvp = None
			if rsvp and rsvp.going:
				initial[person.name] = 'on'
	if guest.eligible_for_dinner:
		if all_on:
			initial['rehearsal'] = 'on'
		else:
			one_going = False
			dinner = Event.objects.get(pk=2)
			for person in people:
				try:
					rsvp_d = Rsvp.objects.get(person=person, event=dinner)
				except Rsvp.DoesNotExist:
					rsvp_d = None
				if rsvp_d and rsvp_d.going:
					one_going = True
			if one_going:
				initial['rehearsal'] = 'on'
	return initial

@login_required(login_url='/rsvp/')
def go_detail(request, guest, first_visit=False):
	# get the people
	people = guest.person_set.all()
	initial = create_initial_form(guest, all_on=first_visit)
	form = EventForm(people=people, initial=initial) 
	context = RequestContext(request, {
		'dinner' : guest.eligible_for_dinner,
		'guest' : guest,
		'people' : people,
		'form': form,
		})
	return render_to_response('rsvp/detail.html', context_instance = context)


@login_required(login_url='/rsvp/')
def go_thanks(request, guest):
	# get the people
	form = PostRsvpForm() 
	context = RequestContext(request, {
		'guest' : guest,
		'form': form,
		})
	logout(request)
	request.session['wedcode'] = guest.wedding_code
	return render_to_response('rsvp/thanks.html', context_instance = context)	


def index(request):
	if request.method == 'POST':
		form = CodeForm(request.POST)
		if form.is_valid():
			email = request.POST['email'].lower()
			code = request.POST['wedding_code'].upper()
			try:
				g = Guest.objects.get(wedding_code=code)
				request.session['wedcode'] = code
			except Guest.DoesNotExist:
				g = None
			if g is None:
				messages.add_message(request, messages.WARNING, _('Sorry, we couldn\'t log you in at this time.'))
				return render(request, '/rsvp/index.html', {'form': form})
			if g.first_visit:
				# create site user
				user = User.objects.create_user(g.name[:29], email, code)
				g.user = user
				g.email = email
				g.first_visit = False
				g.save()
				user = authenticate(username=g.name[:29], password=code)
				if user is not None:
					if user.is_active:
						login(request, user)
						return go_detail(request, g, first_visit=True)
				else:
					messages.add_message(request, messages.WARNING, _('Sorry, we couldn\'t log you in at this time.'))
					return render(request, '/rsvp/index.html', {'form': form})
			else:
				# check against email
				if email != g.email:
					messages.add_message(request, messages.WARNING, _('You\'ve logged in with a different email address. Try again with the correct one.'))
					return render(request, 'rsvp/index.html', {'form': form})
				else:
					user = authenticate(username=g.name[:29], password=code)
					if user is not None:
						if user.is_active:
							login(request, user)
							return go_detail(request, g)
					messages.add_message(request, messages.WARNING, _('Sorry, we couldn\'t log you in at this time.'))
					return render(request, 'rsvp/index.html', {'form': form})

		else:
			return render(request, 'rsvp/index.html', {'form': form})
	else:
		form = CodeForm()
		return render(request, 'rsvp/index.html', {'form': form})


def request_code(request):
	if request.method == 'POST':
		form = RequestForm(request.POST)
		if form.is_valid():
			name = request.POST.get("name", "")
			email = request.POST.get("email", "")
			send_request_email(name, email)
			messages.add_message(request, messages.SUCCESS, _('Your request has been saved. Thanks!'))
			return render(request, 'rsvp/request.html', {'form': form})
		else:
			messages.add_message(request, messages.ERROR, _('There were problems with your request.'))
			return render(request, 'rsvp/request.html', {'form': form})

	else:
		form = RequestForm()

		return render(request, 'rsvp/request.html', {'form': form})


def check_csrf(request):
	return CsrfViewMiddleware().process_view(request, detail, None, None)

def updateForEvent(person, event, request, forceFalse=False):
	try:  # does an rsvp object exists?
		r = Rsvp.objects.get(person=person, event=event)
	except Rsvp.DoesNotExist:
		r = Rsvp(person=person, going=True, event=event)
	if person.name in request.POST and not forceFalse:
		going = True
	else:
		going = False
	person.attending = going
	r.going = going
	person.save()
	r.save()
	return going


def send_rsvp_email(num_yes, email):
	if num_yes > 0:
		html = 'https://s3.amazonaws.com/fieldswedsitemail/email_yes.html'
	else:
		html = 'https://s3.amazonaws.com/fieldswedsitemail/email_no.html'
	req = requests.get(html)
	return requests.post(
        env("DJANGO_MAILGUN_SERVER_NAME") + "/messages",
        auth=("api", env("DJANGO_MAILGUN_API_KEY")),
        data={"from": "El & Raf <wedding@elisabethandrafael.com>",
              "to": email,
              "subject": "We\'ve received your RSVP",
              "text": 'We\'ve received your RSVP - thanks!',
              "html": req.text})


@login_required(login_url='/rsvp/')
def detail(request):
	if request.method == 'POST':
		if check_csrf(request):
			raise PermissionException()
		else:
			number_yes = 0
			code = request.session.get('wedcode')
			g = Guest.objects.get(wedding_code=code)
			people = g.person_set.all();
			event = Event.objects.get(pk=1)
			if g.eligible_for_dinner:
				dinner = Event.objects.get(pk=2)
			else:
				dinner = None
			for person in people:
				if updateForEvent(person, event, request): number_yes += 1
				if g.eligible_for_dinner:
					if 'rehearsal' in request.POST:
						updateForEvent(person, dinner, request)
					else:
						updateForEvent(person, dinner, request, forceFalse=True)
			send_rsvp_email(number_yes, g.email)			
			return go_thanks(request, g)
	else:
		return redirect('/rsvp')


def comment(request):
	if request.method == 'POST':
		form = PostRsvpForm(request.POST)
		code = request.session.get('wedcode')
		g = Guest.objects.get(wedding_code=code)
		if form.is_valid():			
			msg = request.POST.get("comments", "")
			send_post_rsvp_msg(g.name, g.email, msg)
			context = RequestContext(request, {
				'guest' : g,
				})
			messages.add_message(request, messages.SUCCESS, _('Thanks, we received your message.'))
			logout(request)
			return render_to_response('rsvp/thanks.html', context_instance = context)
		else:
			messages.add_message(request, messages.ERROR, _('Sorry, your message could not be sent.'))
			context = RequestContext(request, {
				'guest' : g,
				'form' : form,
				})
			return render_to_response('rsvp/thanks.html', context_instance = context)
	else:
		redirect('/rsvp/')

def get_going_text(going):
	if going:
		return 'Yes'
	else:
		return 'No'


def get_rsvp_admin_data():
	wedding = Event.objects.get(pk=1)
	rsvps = Rsvp.objects.filter(event=wedding)
	stats = {}
	wedding_rsvps = []
	events_interest = []
	wed_going = 0; wed_notgoing = 0; dinner_going = 0; dinner_notgoing = 0; neveracc = 0;
	for rsvp in rsvps:
		if rsvp.going: 
			wed_going += 1
		else:
			wed_notgoing += 1
		r = [rsvp.person.guest.name, rsvp.person.name, get_going_text(rsvp.going), rsvp.modified]
		wedding_rsvps.append(r)
	dinner = Event.objects.get(pk=2)
	rsvps_d = Rsvp.objects.filter(event=dinner)
	dinner_rsvps = []
	for rsvp in rsvps_d:
		if rsvp.going: 
			dinner_going += 1
		else:
			dinner_notgoing += 1
		r = [rsvp.person.guest.name, rsvp.person.name, get_going_text(rsvp.going), rsvp.modified]
		dinner_rsvps.append(r)
	g = Guest.objects.filter(first_visit=True)	
	never_logged_in = []
	for guest in g:
		neveracc += 1
		l = [guest.name]
		never_logged_in.append(l)
	## get interest 
	event_pks = Interest.objects.values_list('event').distinct()
	for pk in event_pks:
		event = Event.objects.get(pk=pk[0])
		interests = Interest.objects.filter(event=event)
		num_conf = interests.count()
		weighted_conf = 0
		for interest in interests:
			gg = interest.guest
			n_rsvps = Rsvp.objects.filter(event=wedding, going=True, person__guest=gg).count()
			weighted_conf += n_rsvps
		r = [event.name, num_conf, weighted_conf]
		events_interest.append(r)
	stats['wed_going'] = wed_going; stats['wed_notgoing'] = wed_notgoing;
	stats['dinner_going'] = dinner_going; stats['dinner_notgoing'] = dinner_notgoing;
	stats['never'] = neveracc
	return wedding_rsvps, dinner_rsvps, never_logged_in, events_interest, stats


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def admin(request):
	wedding, dinner, never, interest, stats = get_rsvp_admin_data()
	context = RequestContext(request, {
		'dinner' : dinner,
		'wedding' : wedding,
		'never' : never,
		'interest' : interest,
		'stats' : stats,
		})
	return render_to_response('rsvp/admin.html', context_instance = context)


def send_post_rsvp_msg(name, email, message):
	body = ("[Name] \n" + name + "\n\n[Email]\n" + email + "\n\n[Message]\n" + message)
	return requests.post(
        env("DJANGO_MAILGUN_SERVER_NAME") + "/messages",
        auth=("api", env("DJANGO_MAILGUN_API_KEY")),
        data={"from": "Wedding Website <mailgun@elisabethandrafael.com>",
              "to": ["wedding@elisabethandrafael.com"],
              "subject": "Post RSVP Message",
              "text": body})


def send_request_email(name, email):
	body = ("[Name] \n" + name + "\n\n[Email]\n" + email)
	return requests.post(
        env("DJANGO_MAILGUN_SERVER_NAME") + "/messages",
        auth=("api", env("DJANGO_MAILGUN_API_KEY")),
        data={"from": "Wedding Website <mailgun@elisabethandrafael.com>",
              "to": ["wedding@elisabethandrafael.com"],
              "subject": "Request for Wedding Code",
              "text": body})


def add_to_rsvp_mailing_list(email):
	return requests.post(
		"https://api.mailgun.net/v3/lists/rsvp@elisabethandrafael.com/members",
		auth=("api", env("DJANGO_MAILGUN_API_KEY")),
		data={'subscribed': True,
              'address': email})


