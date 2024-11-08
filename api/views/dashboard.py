from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from ..utils import render_as_env

# Create your views here.
@require_GET
@login_required(login_url='/auth/login')
def index(request):
    return render_as_env(request, 'index.html')

@require_GET
@login_required(login_url='/auth/login')
def dashboard(request):
    return render_as_env(request, 'dashboard.html')

@require_GET
def not_found(request):
    return render_as_env(request, '404.html')

@require_GET
def for_else(request):
    return redirect('not_found')

urls = [
    path("", index, name="index"),
    path("dashboard", dashboard, name="dashboard"),
    path('404', not_found, name='not_found'),
    re_path(r'^.*\.*', for_else, name='for_else'),
] 