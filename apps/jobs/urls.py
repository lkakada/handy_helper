from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^add/$', views.add, name="add"),
    url(r'^add/job/$', views.add_job, name="add_job"),
    url(r'^move/job/(?P<id>\d+)/$', views.move, name="move"),
    url(r'^view/(?P<id>\d+)/$', views.view, name="view"),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit'),
    url(r'^update/$', views.update, name="update"),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name="delete"),
    url(r'^destroy/$', views.destroy, name="destroy"),
]
