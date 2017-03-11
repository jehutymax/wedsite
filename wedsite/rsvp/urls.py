# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.index,
        name='rsvp'
    ),
    url(
        regex=r'^request/$',
        view=views.request_code,
        name='rsvp_request'
    ),
        url(
        regex=r'^confirmation/$',
        view=views.detail,
        name='rsvp_detail'
    ),
        url(
        regex=r'^comment/$',
        view=views.comment,
        name='rsvp_comment'
    ),
        url(
        regex=r'^admin/$',
        view=views.admin,
        name='rsvp_admin'
    ),
        url(
        regex=r'^(?P<guest_id>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<event_id>\w+)/interest/$',
        view=views.interest,
        name='rsvp_interest'
    ),

]
