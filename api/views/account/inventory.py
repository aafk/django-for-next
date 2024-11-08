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
        'type': item.type,
        'account': str(item.accountID),
        'customer': str(item.customerID),
        'measure': str(item.measureID),
        'avg_price': str(item.avg_price),
        'detail': item.detail,
        'notes': item.notes,
    }

@require_http_methods(['GET', "POST"])
@login_required(login_url="/auth/login")
def index(req):
    if req.method == 'GET':
        return render_as_env(req, 'account/inventory/index.html')
    try:
        method = req.POST['method']
        data = extract_data(req.POST)
        if method == 'read':
            items = [transform_item(item) for item in Inventory.objects.all()]
            return response_as_json(items)
        elif method == "update":
            item = Inventory.objects.get(pk=data['id'])
            form = InventoryForm(data, instance=item)
            return response_using_form(req, form, transform_item)
        elif method == "create":
            form = InventoryForm(data)
            return response_using_form(req, form, transform_item)
        elif method == "delete":
            print(req.POST.getlist('data[]'))
            for id in req.POST.getlist('data[]'):
                Inventory.objects.get(pk=id).delete()
            return HttpResponse()
    except Exception as e:
        return HttpResponseBadRequest(str(e))
        
@require_GET
@login_required(login_url="/login/")
def get(req):
    measures = [{
        'value': item.id,
        'label': item.name
        } for item in Inventory.objects.all()]
    return JsonResponse({
        'data': measures,
    })

urls = [
    path("account/inventory", index, name="account.inventory.index"),
    path("account/inventories", get, name="account.supplier.get"),
]