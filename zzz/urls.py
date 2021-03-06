"""zzz URL Configuration

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
from django.contrib import admin
from django.contrib.auth.models import User
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from leads import views
from leads.models import Lead
from django.db.models.functions import Length

router = routers.DefaultRouter()
router.register(r'leads', views.LeadViewSet)


# Serializers define the API representation.
class LeadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lead
        #fields = ('project_id', 'title', 'description', 'skills', 'url')
        fields = ('id','title', 'description', 'url', 'skills','price', 'bid_details', 'bid_budget', 'bid_days', 'bid_submitted')


# ViewSets define the view behavior.
class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.filter(bid_details__isnull=True)
    serializer_class = LeadSerializer

# ViewSets define the view behavior.
class BidViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.exclude(bid_details__isnull=True).exclude(bid_submitted=True).annotate(bid_length=Length('bid_details')).filter(bid_length__gt=0)
    serializer_class = LeadSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'leads', LeadViewSet)
router.register(r'bids', BidViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('leads.urls')),
]
