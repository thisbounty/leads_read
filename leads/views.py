from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from leads.models import Lead
from leads.serializers import LeadSerializer
from leads.serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework import status, generics


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class LeadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Lead.objects.all().order_by('-project_id')
    serializer_class = LeadSerializer


@csrf_exempt    # TODO: Not save
def lead_list(request):
    """
    List all code leads, or create a new lead.
    """
    if request.method == 'GET':
        snippets = Lead.objects.all()
        serializer = LeadSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LeadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def lead_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        lead = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LeadSerializer(lead)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LeadSerializer(lead, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        lead.delete()
        return HttpResponse(status=204)



class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
