# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=views.contact_form,
        name='contact'
    ),
    url(
        regex=r'^/test$',
        view=views.contact_test,
        name='contact_test'
    ),
]
