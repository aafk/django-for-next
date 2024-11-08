from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST,  require_http_methods
from django.contrib.auth.decorators import login_required
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
        'user_created': item.user_created.username,
        'date_created': item.date_created.strftime('%Y-%m-%d'),
    }

@require_http_methods(['GET', "POST"])
@login_required(login_url="/auth/login")
def index(req):
    if req.method == 'GET':
        return render_as_env(req, 'account/measure/index.html')
    try:
        method = req.POST['method']
        data = extract_data(req.POST)
        if method == 'read':
            accounts = [transform_item(item) for item in Measure.objects.all()]
            return response_as_json(accounts)
        elif method == "update":
            account = Measure.objects.get(pk=data['id'])
            form = MeasureForm(data, instance=account)
            return response_using_form(req, form, transform_item)
        elif method == "create":
            form = MeasureForm(data)
            return response_using_form(req, form, transform_item)
        elif method == "delete":
            print(req.POST.getlist('data[]'))
            for id in req.POST.getlist('data[]'):
                Measure.objects.get(pk=id).delete()
            return HttpResponse()
    except Exception as error:
        return HttpResponseBadRequest(str(error))

@require_GET
@login_required(login_url="/login/")
def get(req):
    suppliers = [{
        'value': item.id,
        'label': item.name
        } for item in Measure.objects.all()]
    return JsonResponse({
        'data': suppliers,
    })


urls = [
    path("account/measure", index, name="account.measure.index"),
    path("account/measures", get, name="account.measure.get"),
]