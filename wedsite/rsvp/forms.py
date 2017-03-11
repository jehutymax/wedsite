from django import forms
from django.utils.translation import ugettext as _

class SoonForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your E-mail*', 'required': '', 'data-validation-required-message': 'Please enter your email address.'}))

class CodeForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your E-mail*'), 'required': '', 'data-validation-required-message': 'Please enter your email address.'}))
	wedding_code = forms.CharField(label="Wedding Code", max_length=12, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Wedding Code*'), 'required': '', 'data-validation-required-message': 'Please enter your wedding invitation code.', 'pattern': '([A-Za-z0-9]){1,12}', 'data-validation-pattern-message': "That doesn't look right."}))

class RequestForm(forms.Form):
	name = forms.CharField(label="Your name", max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Name*'), 'required': '', 'data-validation-required-message': 'Please enter your name.'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your E-mail*'), 'required': '', 'data-validation-required-message': 'Please enter your email address.'}))

class PostRsvpForm(forms.Form):
	comments = forms.CharField(label=_("Comments"), max_length=500, widget=forms.Textarea(attrs={'rows': 5, 'cols': 40, 'style':'resize:none;'}))
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(PostRsvpForm, self).__init__(*args, **kwargs)

class EventForm(forms.Form):
	rehearsal = forms.BooleanField(label="Rehearsal", required=False,
			widget=forms.CheckboxInput(attrs={'data-size': 'small', 'data-on-color': 'success', 'data-off-color': 'info', 'data-on-text': 'Yes, we\'ll be there!', 'data-off-text': 'No, sorry!'}))
	def __init__(self, people, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(EventForm, self).__init__(*args, **kwargs)
		for i in range(0, len(people)):
			self.fields[people[i].name] = forms.BooleanField(required=True,
				widget=forms.CheckboxInput(attrs={'data-size': 'mini', 'data-on-color': 'success', 'data-off-color': 'info', 'data-on-text': 'Yes', 'data-off-text': 'No', }))
