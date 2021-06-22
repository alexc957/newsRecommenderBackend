from django.shortcuts import redirect, render,HttpResponse

# Create your views here.

def redirect_view():
    return HttpResponse('please go to <a href="/graphql">the graphi view </a>')
