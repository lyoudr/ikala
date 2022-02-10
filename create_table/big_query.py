from ikala.custom_res import CustomError

from rest_framework import status

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.api_core import retry

from time import sleep

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
            return self._client.get_table(table_id, retry=retry.Retry(maximum=10))
        except NotFound:
            return None

    def read(self, table_id):
        try:
            query = f"""
                SELECT ROW_NUMBER() OVER() AS id, *
                FROM `{table_id}`
            """
            job_config = bigquery.QueryJobConfig(use_query_cache=False)
            query_job = self._client.query(query, job_config=job_config)
            return [dict(row) for row in query_job]
        except NotFound:
            raise CustomError(
                error_code = 'read_db_err', 
                status_code = status.HTTP_404_NOT_FOUND, 
                err_message = 'can not find data'
            )
    
    def write(self, table, data_rows, retry=10, sleep_time=3):
        """
            because: https://stackoverflow.com/questions/30348384/not-found-table-for-new-bigquery-table
            so, I just retry in 3 seconds once if insert_rows_json raising error.

            Maybe we can find out a more efficient way to handle this API? Consider Bigquery is eventually consistent, dataset and table are so, thus we can not check the table is whether
            created or not, even this person of google bigquery team can not give a good timeframe for this.
        """
        while True:
            try: 
                self._client.insert_rows_json(table, data_rows)
                return
            except Exception:
                retry = retry -1
                if retry == 0:
                    raise CustomError(
                        error_code = 'insert_tb_err', 
                        status_code = status.HTTP_404_NOT_FOUND, 
                        err_message = 'can not find table'
                    )
                sleep(sleep_time) # avoid the high freq. api calling
                continue
        
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
                err_message = str(error)
            )
    

    def create_table(self, table_id):
        try:
            schema = [
                bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("created_at", "DATETIME", mode="REQUIRED")
            ]
            table = bigquery.Table(table_id, schema=schema)
            return self._client.create_table(table)
        except Exception as error:
            raise CustomError(
                error_code = 'create_tb_err', 
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
                err_message = str(error)
            )