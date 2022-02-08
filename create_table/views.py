from create_table.big_query import BigQuery
from ikala.custom_res import CustomError, CustomJsonResponse

from rest_framework import status
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
        if not data.get('created_at'):
            data.update({
                "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S") 
            })
        
        bq =  BigQuery()
        dataset_id = "{}.ikala_super_swe_2022".format(bq._project)
        table_id = "{}.ikala_super_swe_2022.interview_project".format(bq._project)

        # 1. Check if dataset existed
        dataset = bq.get_dataset(dataset_id)
        if not dataset:
            bq.create_dataset(dataset_id)

        # 2. Check if table existed
        table = bq.get_table(table_id)
        if not table:
            table = bq.create_table(table_id)

        # 3. Insert data
        data_rows = [data]
        try:
            bq._client.insert_rows_json(table, data_rows)
            # Read from bigquery to make sure that every data has been written to bq
            result = bq.read()
        except Exception as error:
            raise CustomError(
                error_code = '0001',
                status_code = status.HTTP_400_BAD_REQUEST,
                err_message = str(error)
            )
        
        return CustomJsonResponse(
            re_code = '0000',
            re_data = result,
            status = status.HTTP_200_OK,
            re_message = 'create data successfully'
        )
