from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

import requests
import json
import environ

env = environ.Env()

# Create your views here.
def send_email(name, email, message):
	body = ("[Name] \n" + name + "\n\n[Email]\n" + email + "\n\n[Message]\n" + message)
	return requests.post(
        env("DJANGO_MAILGUN_SERVER_NAME") + "/messages",
        auth=("api", env("DJANGO_MAILGUN_API_KEY")),
        data={"from": "Wedding Website <mailgun@elisabethandrafael.com>",
              "to": ["wedding@elisabethandrafael.com"],
              "subject": "Message from the website",
              "text": body})

def evaluate_captcha(user_response):
	return requests.post(
		"https://www.google.com/recaptcha/api/siteverify",
		{"secret": env("DJANGO_GOOGLE_RECAPTCHA"),
		"response": user_response}).json()

def contact_test(request):
	u_resp = request.POST.get("captchaResponse", "")
	result = evaluate_captcha(u_resp)
	response = {}
	response["status"] = result.get("success", False)
	response["message"] = result.get('error-codes', None) or "Unspecified error."
	print(response)
	return HttpResponse(json.dumps(response), content_type='application/json')

def is_valid_message(name, email, message):
	body = name + email + message
	slimbody = "".join(body.split())

	if not slimbody:
		return False
	else:
		return True

def contact_form(request):
	if (request.method == 'POST'):
		name = request.POST.get("name", "")
		email = request.POST.get("email", "")
		message = request.POST.get("message", "")

		result_data = {}

		if is_valid_message(name, email, message):
			send_email(name, email, message)
			result_data['result'] = "Success"
			result_data['message'] = "Got it! Thanks!"
		else:
			result_data['result'] = "Error"
			result_data['message'] = "Your message didn't go through. Try again."

		return HttpResponse(json.dumps(result_data), content_type="application/json")
	else:
		return HttpResponseRedirect('/')