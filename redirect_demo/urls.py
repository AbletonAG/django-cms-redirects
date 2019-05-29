from django.conf.urls import include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
]
