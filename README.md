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
    - Replace user, pass, db_name accordingly.

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
```py
curl -X POST http://127.0.0.1:8000/example/ -H "Content-Type: application/json" -d "{\"title\": \"My first example\", \"content\": \"This is the content of my first example\"}"
```

### Read All
List all records:
```py
curl -X GET http://127.0.0.1:8000/example/
```

### Read
Get a single record:
```py
curl -X GET http://127.0.0.1:8000/example/1
```

### Update
Change an existing record:
```py
curl -X PUT http://127.0.0.1:8000/example/1 -H "Content-Type: application/json" -d "{\"title\": \"My first updated example\", \"content\": \"This is the updated content of my first example\"}"
```

### Delete
Delete a single record:
```py
curl -X DELETE http://127.0.0.1:8000/example/1
```

### Delete All
Delete all records:
```py
curl -X DELETE http://127.0.0.1:8000/example/
```

# LANGUAGE SUPPORT
You can enable multilingual support in the API. To do this, **copy** one of the language files from the locales folder, **rename** the class to match the desired ISO country code, and **translate** the properties. 

You can then use the new language class in your routers as follows:

```py
@router.get("/", response_model=List[schemas.Example])
async def read_all(
    request: Request, # inject Request from FastApi
    db: AsyncSession = Depends(database.get_db)
):
    Lang = get_lang(request) # Get specified language
    print(Lang.example)
    ...
```
The language must be sent in the request header:
```py
curl -X GET http://127.0.0.1:8000/example/ -H "Accept-Language: de"
```