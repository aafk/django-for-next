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
        'active': item.active,
        'company': item.company,
        'accupation': item.accupation,
        'mobile1': item.mobile1,
        'mobile2': item.mobile2,
        'address': item.address,
    }

@require_http_methods(['GET', "POST"])
@login_required(login_url="/auth/login")
def index(req):
    if req.method == 'GET':
        return render_as_env(req, 'account/customer/index.html')
    try:
        method = req.POST['method']
        data = extract_data(req.POST)
        if method == 'read':
            accounts = [transform_item(item) for item in Person.objects.filter(person_role=True)]
            return response_as_json(accounts)
        elif method == "update":
            account = Person.objects.get(pk=data['id'])
            form = CustomerForm(data, instance=account)
            return response_using_form(req, form, transform_item)
        elif method == "create":
            form = CustomerForm(data)
            return response_using_form(req, form, transform_item)
        elif method == "delete":
            print(req.POST.getlist('data[]'))
            for id in req.POST.getlist('data[]'):
                Person.objects.get(pk=id).delete()
            return HttpResponse()
    except Exception as error:
        return HttpResponseBadRequest(str(error))
        
@require_GET
@login_required(login_url="/login/")
def get(req):
    customers = [{
        'value': item.id,
        'label': item.name
        } for item in Person.objects.filter(person_role=True)]
    return JsonResponse({
        'data': customers,
    })

urls = [
    path("account/customer", index, name="account.customer.index"),
    path("account/customers", get, name="account.customer.get"),
]