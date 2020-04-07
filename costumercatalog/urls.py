import json

from django.contrib import admin
from django.urls import path
from costumers.views import Costumers


urlpatterns = [
    path('admin/', admin.site.urls),
]

with open('/home/oem/DSN/tkt/costumercatalog/mock_data.json') as jsonfile:
    data = json.load(jsonfile)
    for costumer in data:
        Costumers.save(costumer)