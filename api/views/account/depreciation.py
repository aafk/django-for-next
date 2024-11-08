from django.http import  HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET,  require_http_methods
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import date
from django.urls import path
from api.forms import *
from api.models import *
from api.utils import *

def extract_data(body):
    return dict((key[5:-1], body[key]) for key in body.keys() if key.startswith("data"))

def transform_item(item):
    return {
        'id': item.id,
        'name': item.name,
        'type': item.type,
        'brand': item.brand,
        'account': str(item.accountID),
        'level': str(item.levelID),
        'price': str(item.price),
        'purchase_month': item.purchase_month.strftime('%Y-%m'),
        'notes': item.notes,
        'detail': item.detail,
        'depreciation': item.depreciation,
    }

@require_http_methods(['GET', "POST"])
@login_required(login_url="/auth/login")
def index(req):
    if req.method == 'GET':
        return render_as_env(req, 'account/depreciation/index.html')
    try:
        method = req.POST['method']
        data = extract_data(req.POST)
        if method == 'read':
            items = [transform_item(item) for item in Depreciation.objects.all()]
            return response_as_json(items)
        elif method == "update":
            item = Depreciation.objects.get(pk=data['id'])
            form = DepreciationForm(data, instance=item)
            return response_using_form(req, form, transform_item)
        elif method == "create":
            form = DepreciationForm(data)
            return response_using_form(req, form, transform_item)
        elif method == "delete":
            print(req.POST.getlist('data[]'))
            for id in req.POST.getlist('data[]'):
                Depreciation.objects.get(pk=id).delete()
            return HttpResponse()
    except Exception as e:
        return HttpResponseBadRequest(str(e))
        
@require_GET
@login_required(login_url="/login/")
def get(req):
    depreciations = [{
        'value': item.id,
        'label': item.name
        } for item in DepreciationLevel.objects.all()]
    return JsonResponse({
        'data': depreciations,
    })

urls = [
    path("account/depreciation", index, name="account.depreciation.index"),
    path("account/depreciations", get, name="account.depreciation.get"),
]