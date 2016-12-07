from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('title', 'description', 'skills', 'price', 'url')


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Lead.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'leads')    # ???


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
