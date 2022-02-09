from ikala.custom_res import CustomError

from rest_framework import status

from google.cloud import bigquery
from google.cloud.exceptions import NotFound

class BigQuery:

    def __init__(self):
        self._client = bigquery.Client()
        self._project = bigquery.Client().project

    def get_dataset(self, dataset_id):
        try:
            return self._client.get_dataset(dataset_id)
        except NotFound:
            return None

    def get_table(self, table_id):
        try:
            return self._client.get_table(table_id)
        except NotFound:
            return None

    def read(self, table_id):
        try:
            query = f"""
                SELECT ROW_NUMBER() OVER() AS id, *
                FROM `{table_id}`
            """
            query_job = self._client.query(query)
            return [dict(row) for row in query_job]
        except NotFound:
            raise CustomError(
                error_code = 'read_db_err', 
                status_code = status.HTTP_404_NOT_FOUND, 
                err_message = 'read error'
            )
    
    def write(self, table, data_rows):
        errors = self._client.insert_rows_json(table, data_rows)
        # Read from bigquery to make sure that every data has been written to bq
        if errors != []:
            raise CustomError(
                error_code = 'insert_tb_err', 
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
                err_message = 'insert data to table failed'
            )

    def create_dataset(self, dataset_id):
        try:
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "US"
            dataset = self._client.create_dataset(dataset, timeout=30)
            return dataset
        except Exception as error:
            raise CustomError(
                error_code = 'create_db_err', 
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
                err_message = f'{error}'
            )
    

    def create_table(self, table_id):
        try:
            schema = [
                bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("created_at", "DATETIME", mode="REQUIRED")
            ]
            table = bigquery.Table(table_id, schema=schema)
            table = self._client.create_table(table)
            return table
        except Exception as error:
            raise CustomError(
                error_code = 'create_tb_err', 
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
                err_message = f'{error}'
            )