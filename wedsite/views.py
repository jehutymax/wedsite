from django.shortcuts import render
from django.http import HttpResponseRedirect


# Create your views here.
def send_email(name, email, message):
	return requests.post(
        "https://api.mailgun.net/v3/elisabethandrafael.com/messages",
        auth=("api", "MAILGUN_KEY"),
        data={"from": "Excited User <mailgun@elisabethandrafael.com>",
              "to": ["bar@example.com", "rafaelcdn@gmail.com"],
              "subject": "Hello",
              "text": name + email + message + "Testing some Mailgun awesomness!"})

def contact_form(request):
	name = request.POST.get("name", "")
	email = request.POST.get("email", "")
	message = request.POST.get("message", "")

	send_email(name, email, message)

	




