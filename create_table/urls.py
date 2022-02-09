from django.urls import path

from create_table.views import CreateTable

urlpatterns = [
    path('/bigquery/create_table', CreateTable.as_view(), name = 'create_table'),
]