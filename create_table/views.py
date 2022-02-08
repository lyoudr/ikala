from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from create_table.dataset import BigQuery

from google.cloud.exceptions import NotFound
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
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S") 
        })
        
        bq =  BigQuery()

        dataset_id = "{}.ikala_super_swe_2022".format(bq._project)
        table_id = "{}.ikala_super_swe_2022.interview_project".format(bq._project)
        
        # 1. Check if dataset existed
        try:
            bq.chk_dataset(dataset_id)
            print("Dataset {} already exists".format(dataset_id))
        except NotFound:
            print("Dataset {} is not found".format(dataset_id))
            bq.create_dataset()

        # 2. Check if table existed
        try:
            table = bq.chk_table(table_id)
            print("Tablet {} already exists".format(table_id))
        except NotFound:
            print("Table {} is not found.".format(table_id))
            table = bq.create_table()
        
        data_rows = [data]
        bq._client.insert_rows_json(table, data_rows)

        # Read from bigquery to make sure that every data has been written to bq
        result = bq.read()
        
        return Response(result)
