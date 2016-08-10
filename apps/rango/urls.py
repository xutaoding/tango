from django.conf.urls import url
from django.views import static

import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^like_category/$', views.like_category, name='like_category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),

    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/', views.user_logout, name='logout'),
]

