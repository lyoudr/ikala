from google.cloud import bigquery

class BigQuery:

    def __init__(self):
        # Construct a BigQuery client object.
        self._client = bigquery.Client()
        self._project = bigquery.Client().project

    def chk_dataset(self, dataset_id):
        self._client.get_dataset(dataset_id)  # Make an API request.

    def chk_table(self, table_id):
        return self._client.get_table(table_id)

    def read(self):
        query = f"""
            SELECT ROW_NUMBER() OVER() AS id, *
            FROM `{self._project}.ikala_super_swe_2022.interview_project`
        """
        query_job = self._client.query(query)
        return [row for row in query_job]

    def create_dataset(self):
        # Set dataset_id to the ID of the dataset to create.
        dataset_id = "{}.ikala_super_swe_2022".format(self._project)
        # Construct a full Dataset object to send to the API.
        dataset = bigquery.Dataset(dataset_id)
        # TODO(developer): Specify the geographic location where the dataset should reside.
        dataset.location = "US"
        dataset = self._client.create_dataset(dataset, timeout=30)  # Make an API request.
    
    def create_table(self):
        table_id = "{}.ikala_super_swe_2022.interview_project".format(self._project)
        schema = [
            bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("created_at", "DATETIME", mode="REQUIRED")
        ]
        table = bigquery.Table(table_id, schema=schema)
        table = self._client.create_table(table)  # Make an API request.
        print(
            "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
        )
        return table