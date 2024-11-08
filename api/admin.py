from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AccountLevel)
admin.site.register(Account)

admin.site.register(DepreciationLevel)
admin.site.register(Depreciation)
admin.site.register(DepreciationProgress)
admin.site.register(DepreciationYear)

admin.site.register(Person)
admin.site.register(Measure)
admin.site.register(Inventory)

admin.site.register(Document)
admin.site.register(Transaction)
