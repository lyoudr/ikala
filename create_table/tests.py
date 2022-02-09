from create_table.big_query import BigQuery
from ikala.custom_res import CustomError
from django.test import TestCase, Client

from datetime import datetime

class CreateTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.bq = BigQuery()
        cls.dataset_id = f"{cls.bq._project}.test_dataset"
        cls.table_id = f"{cls.dataset_id}.test_table" 

    # test create dataset
    def test_create_dataset(self):
        try:
            dataset = self.bq.get_dataset(self.dataset_id)
            if not dataset:
                dataset = self.bq.create_dataset(self.dataset_id)
            self.assertTrue(dataset)
        except CustomError:
            pass

    # test create table
    def test_create_table(self):
        try:
            table = self.bq.get_table(self.table_id)
            if not table:
                table = self.bq.create_table(self.table_id)
            self.assertTrue(table)
        except CustomError:
            pass
    
    # test read
    def test_read(self):
        try:
            resp = self.bq.read(self.table_id)
            dataset = self.bq.get_dataset(self.dataset_id)
            table = self.bq.get_table(self.table_id)
            if dataset and table:
                self.assertIsNotNone(resp)
        except CustomError:
            pass

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
        self.assertEqual(res.json().get('re_code'), 'api_success')
        