# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from wedsite.sitemaps import StaticViewSitemap
from wedsite import views

sitemaps = {
    'static': StaticViewSitemap,
}

# Translateable URLs
urlpatterns = i18n_patterns(
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^story/$', TemplateView.as_view(template_name='pages/story.html'), name="story"),
    url(r'^event/$', TemplateView.as_view(template_name='pages/event.html'), name="event"),
    url(r'^travel/$', TemplateView.as_view(template_name='pages/travel.html'), name="travel"),
    url(r'^registry/$', TemplateView.as_view(template_name='pages/registry.html'), name="registry"),
    url(r'^contact-form/', include('wedsite.contact.urls')),
    url(r'^rsvp/', include('wedsite.rsvp.urls')),
    #sitemaps
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
)

urlpatterns += [
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("wedsite.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(r'^i18n/', include('django.conf.urls.i18n')),

    #dynamic assets
    url(r'^css/et-line-font.css$', TemplateView.as_view(template_name='css/et-line-font.css', content_type='text/css'), name="etlinefont"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
    ]
