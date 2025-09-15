# INSTALL

```
$ python -m venv venv
$ source venv/bin/activate

$ pip install --upgrade pip
$ pip install -r requirements.txt
```

# SETUP

- Create an empty Postgres Database.

- Create an `.env` file.
    - Copy and paste the following line into the `.env` file:
        ```
        DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db_name
        ```
    - Replace user, pass, db_name accordingly:

- Create tables:
    ```
    $ python migrate.py
    ```

# RUN

```
$ uvicorn main:app --reload
```

# USAGE

### Create
Insert a new record:
```
$ curl -X POST http://127.0.0.1:8000/example/ -H "Content-Type: application/json" -d "{\"title\": \"My first example\", \"content\": \"This is the content of my first example\"}"
```

### Read All
List all records:
```
$ curl -X GET http://127.0.0.1:8000/example/
```

### Read
Get a single record:
```
$ curl -X GET http://127.0.0.1:8000/example/1
```

### Update
Change an existing record:
```
$ curl -X PUT http://127.0.0.1:8000/example/1 -H "Content-Type: application/json" -d "{\"title\": \"My first updated example\", \"content\": \"This is the updated content of my first example\"}"
```

### Delete
Delete a single record:
```
$ curl -X DELETE http://127.0.0.1:8000/example/1
```

### Delete All
Delete all records:
```
$ curl -X DELETE http://127.0.0.1:8000/example/
```
