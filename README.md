## IKALA SWE Interview App
---
An app which provides API about creating dataset and table and inserting data to Bigquery


### 1. Create a Linux VM on GCE
- Create Linux VM on compute engine
- Version: Ubuntu 20.04 LTS
- Firewall: allow HTTP traffic

### 2. Create Service account 
- Create a service account
- Grant **My Project > Owner** role to this service account
- Download its JSON Key file credential
- Set the environment variable **GOOGLE_APPLICATION_CREDENTIALS** to the path of this JSON file

### 3. Service
#### **(1) Install required libraries**
- Install required libraries and other required libraries described in ./requirement.txt
    ```
    pip install --upgrade google-cloud-bigquery
    ```

#### **(2) Django**
- Create app **create_table** 
- Write Class **BigQuery** in ./create_table/big_query.py, use `google-cloud-bigquery` library to communicate with bigquery by using its method: `get_dataset`, `get_table`, `create_dataset`, `create_table`, `query`
- Create **CreateTable** APIView in ./create_table/views.py
- Use POST method in this view.
- Request body: Json format, ex:
    ```
    {
        "name": "Ann"
        "age": 28
    }
    ```
- POST method code logic:
    - check if dataset is existed, if it is not, create it.
    - check if table is exist, if it is not, create it.
    - write user post data to the table "**{project}.ikala_super_swe_2022.interview_project**"
    - read and return all rows from Bigquery table to make sure that the new data has been inserted to the table 
- Define **CustomJsonRespone**, **CustomError** in ./ikala/custom_res.py and use these Class to return custom response and custom error message

#### **(3) Docker-Compose**
- For the convenience of deploying the project to GCE and its environment setting, I built the Django app in a docker container and set relevant environment variable.
- I use Docker-Compose to deinfe three services: Nginx, Django, PostgreSQL
- Nginx serves as a web server to route request to Django and provide static files of Swagger
- uWSGI wrapped Django server, and allows communication between Django server and Nginx
- PostgreSQL serves as a database to store basic data
- Start the app by running 
    ```
    docker-compose up -d 
    ```

### 4. **Testing**
- In order to verify the correctness of the app, I wrote testing
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
### 5. GitHub Actions CI
- About Continous Integration, I use **GitHub Actions**
- Create a config file in .github/workflows/ikala.yml
- Github Actions will set required environmetn and run command `python manage.py test` according to this config file
- Testing result success:
![image](https://github.com/lyoudr/ikala/blob/dev/test.png)

### 6. Code Base in GitHub
- Please refer to my github [my github](https://github.com/lyoudr/ikala)
### 7. Test API
#### **(1) API Spec**
- Domain/IP: 34.81.253.216
- Url: http://34.81.253.216/api/bigquery/create_table
- Method: POST
- Request body format: Json, 
- No Token needed
    ```
    {
        "name": "Amy",
        "age": 20
    }
    ```
#### **(2) Success Response**
|  status code   |  re_code     | re_message               | re_data  |
| :-------------:| :----------- | :----------------------- | :-------:|
|   200          |  api_success | create data successfully | {data}   |
#### **(3) Error Code Definition**
|  error code   |  status code   |   error messages            |
| :------------ | :------------:| :-------------------------- |
| read_db_err   |      404      | can not find data           |
| insert_tb_err |      500      | insert data to table failed |
| create_db_err |      500      | error message               |
| create_tb_err |      500      | error message               |
#### **(4) Curl to call this API**
- Please curl this api url to get result http://34.81.253.216/api/bigquery/create_table
    ```
    curl -X POST "http://34.81.253.216/api/bigquery/create_table" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"name\": \"John\",  \"age\": 18}"
    ```
#### **(5) Swagger page**
- You can also test this api in my swagger page
    http://34.81.253.216/swagger/
