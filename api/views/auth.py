from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import path
from ..utils import render_as_env
from ..models import *

# Create your views here.
@require_http_methods(["GET", "POST"])
def login_account(req):
    if req.method == 'GET':
        return render_as_env(req, 'auth/login.html')
    try:
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return JsonResponse({
                'username': req.user.username
            })
        else:
            return HttpResponseNotFound()
    except:
        return HttpResponseBadRequest()
    
@require_GET
@login_required(login_url="/auth/login")
def verify_account(req):
    if req.user.is_authenticated:
        return JsonResponse({
            'username': req.user.username
        })
    else:
        return HttpResponse('Unauthorized', status=401)

csrf_exempt
@require_GET
@login_required(login_url="/auth/login")
def logout_account(req):
    try:
        logout(req)
        return HttpResponse('Success')
    except:
        return HttpResponse('Unauthorized', status=401)

urls = [
    path("login", login_account, name="login_account"),
    path("verify", verify_account, name="verify_account"),
    path("logout", logout_account, name="logout_account"),
]