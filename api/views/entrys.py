from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponse, HttpResponseBadRequest
from ..utils import render_as_env
from ..forms import *
from ..models import *

@require_http_methods(["GET", 'POST'])
@login_required(login_url="/auth/login")
def entry_journal(req):
    if req.method == "GET":
        return render_as_env(req, 'entry/journal.html')
    else:
        form = DepreciationForm(req.POST)
        if form.is_valid() :
            form.save(req.user.id)
            return HttpResponse()
        else:
            field = list(form.errors.keys())[0]
            message = "%s : %s"%(field, form.errors[field][0])
            return HttpResponseBadRequest(message)