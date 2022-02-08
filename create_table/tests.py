from create_table.big_query import BigQuery
from django.test import TestCase, Client

from datetime import datetime

class CreateTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.bq = BigQuery()
        cls.dataset_id = f"{cls.bq._project}.test_dataset"
        cls.table_id = f"{cls.bq._project}.test_dataset.test_table" 

    # test create dataset
    def test_create_dataset(self):
        dataset = self.bq.get_dataset(self.dataset_id)
        if not dataset:
            dataset = self.bq.create_dataset(self.dataset_id)
        self.assertTrue(dataset)

    # test create table
    def test_create_table(self):
        table = self.bq.get_table(self.table_id)
        if not table:
            table = self.bq.create_table(self.table_id)
        self.assertTrue(table)
    
    # test read
    def test_read(self):
        resp = self.bq.read()
        dataset = self.bq.get_dataset(self.dataset_id)
        table = self.bq.get_table(self.table_id)
        if dataset and table:
            self.assertIsNotNone(resp)
        else:
            self.assertIsNone(resp)

    # test create_table api
    def test_api(self):
        c = Client()
        data = {
            'name': 'Ann',
            'age': 28,
            'created_at': datetime.now().strftime("%Y-%m-%dT%H:%M:%S") 
        }
        res = c.post('/api/bigquery/create_table', data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json().get('re_code'), '0000')
        