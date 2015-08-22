from django.shortcuts import render, get_object_or_404, redirect

# GG imports
from .models import Url
from .forms import UrlForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UrlSerializer
from rest_framework import generics
import requests
import bs4
from selenium import webdriver
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from mysite import settings


# Create your views here.
@login_required(login_url='/urlexpand/accounts/login/')
@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET', 'POST'])
def rest_url_list(request, format=None):
	if request.method == 'GET':
		urls = Url.objects.all()
		serializer = UrlSerializer(urls, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		serializer = UrlSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/urlexpand/accounts/login/')
@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET', 'PUT', 'DELETE'])
def rest_url_detail(request, pk, format=None):
	try:
		url = Url.objects.get(pk=pk)
	except Url.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = UrlSerializer(url)
		return Response(serializer.data)
	elif request.method == 'PUT':
		serializer = UrlSerializer (url, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		url.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)



@login_required(login_url='/urlexpand/accounts/login/')
@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['POST', ])
def newimage(request, pk, format=None):
	url = get_object_or_404(Url, pk=pk)
	if request.method == 'POST':
		url.newimage()
	

@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='/urlexpand/accounts/login/')
def url_list(request):
	urls = Url.objects.all()
	return render(request, 'urlexpand/urlexpand.html', {'urls' : urls})

@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='/urlexpand/accounts/login/')
def url_detail(request, pk):
	url = get_object_or_404(Url, pk=pk)
	return render(request, 'urlexpand/urldetails.html', {'url': url})

@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='/urlexpand/accounts/login/')
def url_add(request):
	if request.method == "POST":
		form = UrlForm(request.POST)
		if form.is_valid():
			url = form.save(commit=False)
			url.create()
			return redirect('urlexpand.views.url_detail', pk=url.pk)
	else:
		form = UrlForm()
	return render(request, 'urlexpand/urladd.html', {'form': form})

@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='/urlexpand/accounts/login/')
def url_remove(request, pk):
	url = get_object_or_404(Url, pk=pk)
	url.delete()
	return redirect('urlexpand.views.url_list')
