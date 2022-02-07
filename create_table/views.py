from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from create_table.dataset import BigQuery

from datetime import datetime

class CreateTable(APIView):
    @swagger_auto_schema(
        operation_summary = 'create table',
        request_body = openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties = {
                'name': openapi.Schema(
                    type = openapi.TYPE_STRING,
                    description = 'name',
                ),
                'age': openapi.Schema(
                    type = openapi.TYPE_INTEGER,
                    description = 'age',
                )
            }
        )
    )
    def post(self, request):
        data = request.data
        data.update({
            "id": 1,
            "created_at": '2022-02-07T17:50:30' #datetime.now()
        })
        print('data is =>', data)
        big_query =  BigQuery()
        big_query.create_dataset()
        table = big_query.create_table()
        rows_to_insert = [data]
        big_query._client.insert_rows_json(table, rows_to_insert)
        return Response(data)
