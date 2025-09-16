import argparse
import asyncio
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, Base
from app.models import User
from passlib.context import CryptContext

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        def sync_inspect(connection):
            insp = inspect(connection)
            print("Table(s) in the DB according to the inspector:", insp.get_table_names())
        await conn.run_sync(sync_inspect)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        result = await session.execute(select(User))
        users_exist = result.first() is not None

        if not users_exist:
            parser = argparse.ArgumentParser(description="Initialize the DB")
            parser.add_argument("--username", required=True, help="Username for default user")
            parser.add_argument("--password", required=True, help="Password for default user")
            args = parser.parse_args()
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            hashed_password = pwd_context.hash(args.password)
            new_user = User(username=args.username, password=hashed_password)
            session.add(new_user)
            await session.commit()
            print(f"Default user '{args.username}' created.")

    await engine.dispose()
    print("DB initialization complete.")

if __name__ == "__main__":
    asyncio.run(init_db())
