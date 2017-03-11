from django.contrib import admin

# Register your models here.
from .models import Guest, Person, Event, Rsvp, Interest

class PeopleInline(admin.TabularInline):
	model = Person
	extra = 1

class GuestAdmin(admin.ModelAdmin):
	inlines = [PeopleInline]
	list_display = ('name', 'wedding_code', 'eligible_for_dinner')
	list_filter = ['name']
	search_fields = ['name']


admin.site.register(Guest, GuestAdmin)
admin.site.register(Event)
admin.site.register(Rsvp)
admin.site.register(Interest)
