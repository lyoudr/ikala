## Ikala SWE InterView 
---
An App which provides API about adding dataset and querying BigQuery


### 1. Create a Linux VM on GCE
- create Linux VM on compute engine
- version: Ubuntu 20.04 LTS
- firewall: allow HTTP traffic

### 2. Create Service account 
- create a service account
- grant **My Project > Owner** role to this service account
- download its credentials, a JSON Key file
- Set the environment variable **GOOGLE_APPLICATION_CREDENTIALS** to the path of the JSON file

### 3. Service
#### (1) Install required libraries
- Install required libraries and other required libraries descriped in ./requirement.txt
    ```
        pip install --upgrade google-cloud-bigquery
    ```

#### (2) Django
- Create app **create_table** 
- Write Class **BigQuery** in ./create_table/big_query.py, use `google-cloud-bigquery` library to communicate with bigquery by using its method: `get_dataset`, `get_table`, `create_dataset`, `create_table`, `query`
- Create **CreateTable** APIView in ./create_table/views.py
- Use post method in this view.
- Request body: json format, ex:
    ```
    {
        "name": "Ann"
        "age": 28
    }
    ```
- Post method code logic:
    - check if dataset is existed, if it is not, create it.
    - check if table is exist, if it is not, create it.
    - write user post data to created table : **{project}.ikala_super_swe_2022.interview_project**
    - read data from bigquery to make sure that the new data has been inserted to the table
    - return the data read from bigquery 
 
- Define **CustomJsonRespone**, **CustomError** in ./ikala/custom_res.py and use these Class to return response and error message

#### (3) Docker-compose
- For the convenience of environment setting, I package the Django app in docker and set relevant environment variable.
- Including three containers: Nginx, Django, PostgreSQL
- Nginx as a web server to route request to Django and serve its static files of swagger api
- In order to communicate with Nginx, use uwsgi to start Django app
- PostgreSQL as a database to store basic data
- Start the app by running 
    ```
    docker-compose up -d 
    ```

### 4. Testing
- In order to verify the correctness of code, I write testing
- Use Django Test to do testing
- Write **CreateTableTest** in ./create_table/test.py to define unit test and api test
- Test logic:
    - test create dataset
    - test create table
    - test read table
    - test calling api 
- Run test 
    ```
    python manage.py test
    ```

### 5. Code Base : GitHub
- Please refer my github [my github](https://github.com/lyoudr/ikala)


### 6. Test API
#### (1) Domain
- 34.81.253.261
#### (2) API url
- Please curl this api url to get result http://34.81.253.216/api/bigquery/create_table
    ```
    curl -X POST "http://34.81.253.216/api/bigquery/create_table" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"name\": \"John\",  \"age\": 18}"
    ```
#### (3) Swagger page
- can also test this api in my swagger page
    http://34.81.253.216/swagger/
