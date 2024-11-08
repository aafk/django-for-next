from django.urls import path, include
from .views import auth, dashboard, account, entry

urlpatterns = [

    path('auth/', include(auth.urls)),

    path('', include(account.other.urls)),
    path('', include(account.measure.urls)),
    path('', include(account.customer.urls)),
    path('', include(account.supplier.urls)),
    path('', include(account.inventory.urls)),
    path('', include(account.depreciation.urls)),

    path('', include(entry.journal.urls)),

    path('', include(dashboard.urls)),
]