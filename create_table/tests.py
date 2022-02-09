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
        cls.client = Client()
        cls.data = {
            'name': 'Ann',
            'age': 1,
            'created_at': datetime.now().strftime("%Y-%m-%dT%H:%M:%S") 
        }

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
    
    def assert_api(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json().get('re_code'), 'api_success')

    # test create_table api
    def test_api_once(self):
        res = self.client.post('/api/bigquery/create_table', self.data)
        self.assert_api(res)
    
    # test api erro rate
    def test_api_error_rate(self):
        error_rate = 0
        error_msg = []
        data = self.data
        for i in range(0, 10):
            try:
                data['age'] += 1
                # add data to table
                self.assert_api(self.client.post('/api/bigquery/create_table', data))
                # delete dataset after each insertion
                self.assert_api(self.client.delete('/api/bigquery/create_table'))
            except Exception as error:
                error_rate += 1
                error_msg.append(str(error))
        print(f'error rate is => {error_rate/10 *100}%')
        print(error_msg)

        