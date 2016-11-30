from django.conf.urls import url
from leads import views

urlpatterns = [
    url(r'^leads/$', views.lead_list),
    url(r'^leads/(?P<pk>[0-9]+)/$', views.lead_detail),
]

