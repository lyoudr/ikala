from google.cloud import bigquery

class BigQuery:

    def __init__(self):
        # Construct a BigQuery client object.
        self._client = bigquery.Client()

    def create_dataset(self):
        # Set dataset_id to the ID of the dataset to create.
        print('self._client.project is =>', self._client.project)
        dataset_id = "{}.ikala_super_swe_2022".format(self._client.project)

        # Construct a full Dataset object to send to the API.
        dataset = bigquery.Dataset(dataset_id)

        # TODO(developer): Specify the geographic location where the dataset should reside.
        dataset.location = "US"

        # Send the dataset to the API for creation, with an explicit timeout.
        # Raises google.api_core.exceptions.Conflict if the Dataset already
        # exists within the project.
        dataset = self._client.create_dataset(dataset, timeout=30)  # Make an API request.
        print("Created dataset {}.{}".format(self._client.project, dataset.dataset_id))
    
    def create_table(self):
        table_id = "{}.ikala_super_swe_2022.interview_project".format(self._client.project)
        schema = [
            bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
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