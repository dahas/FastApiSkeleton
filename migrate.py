# 1. Create Postgres DB manually
# 2. Create Models in models.py
# 3. Run: "$ python migrate.py"

import asyncio
from sqlalchemy import inspect
from app.database import engine, Base

from app.models import *

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        def sync_inspect(connection):
            insp = inspect(connection)
            print("Table(s) in the DB according to the inspector:", insp.get_table_names())

        await conn.run_sync(sync_inspect)

    await engine.dispose()
    print("Table(s) created successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
