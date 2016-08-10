"""tango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from registration.backends.simple import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^rango/', include('apps.rango.urls', namespace='rango'))
]

# Notice that `django.conf.urls.patterns` function is deprecated
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})
        # url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, prefix='django.views.static')
    ]
