import os, environ
from pathlib import Path
from django.shortcuts import render
# from django_nextjs.render import render_nextjs_page_sync
from django.http import HttpResponse
from json import dumps

env = environ.Env(
    DEBUG=(bool, True)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env('DEBUG')

def render_as_env(*args, **kwargs):
    # if not DEBUG:
    #     return render_nextjs_page_sync(*args, **kwargs)
    # else:
    return render(*args, **kwargs)
    
def response_as_json(data):
    return HttpResponse(dumps(data),  content_type="application/json")

def response_using_form(req, form, transform_item):
    if form.is_valid() :
        res = form.save(req.user.id)
        return HttpResponse(dumps(transform_item(res)), content_type="application/json")
    else:
        field = list(form.errors.keys())[0]
        message = "%s : %s"%(field, form.errors[field][0])
        raise ValueError(message)