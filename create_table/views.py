from create_table.serializers import CreateTableSerializer
from create_table.big_query import BigQuery
from ikala.custom_res import CustomError, CustomJsonResponse

from rest_framework import status
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from datetime import datetime

class CreateTable(APIView):
    serializer_class = CreateTableSerializer

    @swagger_auto_schema(
        operation_summary = 'create_table_01',
        request_body = openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties = {
                'name': openapi.Schema(
                    type = openapi.TYPE_STRING,
                    description = 'name',
                    example = 'Ann',
                ),
                'age': openapi.Schema(
                    type = openapi.TYPE_INTEGER,
                    description = 'age',
                    example = 20,
                )
            }
        )
    )
    def post(self, request):
        data = request.data
        # validate data
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception = True)

        # default created_at is today
        if not data.get('created_at'):
            data.update({
                "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S") 
            })
        
        bq =  BigQuery()
        dataset_id = "{}.ikala_super_swe_2022".format(bq._project)
        table_id = "{}.interview_project".format(dataset_id)

        # 1. Check if dataset is existed
        if not bq.get_dataset(dataset_id):
            bq.create_dataset(dataset_id)

        # 2. Check if table is existed
        table = bq.get_table(table_id)
        if not table:
            table = bq.create_table(table_id)
        
        # 3. Insert data and read result from table
        data_rows = [data]
        bq.write(table, data_rows, sleep_time=10)
        result = bq.read(table_id)

        return CustomJsonResponse(
            re_code = 'api_success',
            re_data = result,
            status = status.HTTP_200_OK,
            re_message = 'create data successfully'
        )


    @swagger_auto_schema(
        operation_summary = 'delete_dataset_02',
    )
    def delete(self, request):
        """
            I create this API, in convenience of deleting dataset, and can test 'create_table_01' again
        """
        try:
            bq =  BigQuery()
            dataset_ids = (
                "{}.ikala_super_swe_2022".format(bq._project), 
                "{}.test_dataset".format(bq._project)
            )
            for dataset_id in dataset_ids:
                bq._client.delete_dataset(
                    dataset_id, delete_contents=True, not_found_ok=True
                ) 
            return CustomJsonResponse(
                re_code = 'api_success',
                re_data = 'delete dataset successfully',
                status = status.HTTP_200_OK,
                re_message = 'delete dataset successfully'
            )
        except Exception as error:
            raise CustomError(
                error_code = 'delete_db_err', 
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
                err_message = f'{error}'
            )
