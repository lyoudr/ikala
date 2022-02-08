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

    def read(self):
        try:
            query = f"""
                SELECT ROW_NUMBER() OVER() AS id, *
                FROM `{self._project}.ikala_super_swe_2022.interview_project`
            """
            query_job = self._client.query(query)
            return [dict(row) for row in query_job]
        except NotFound:
            return None


    def create_dataset(self, dataset_id):
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        dataset = self._client.create_dataset(dataset, timeout=30)
        return dataset
    

    def create_table(self, table_id):
        schema = [
            bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("created_at", "DATETIME", mode="REQUIRED")
        ]
        table = bigquery.Table(table_id, schema=schema)
        table = self._client.create_table(table)
        print(
            "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
        )
        return table