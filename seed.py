import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def seed():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        # Create schemas
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS tenant_poc_a"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS tenant_poc_b"))

        # Create tasks table in each schema
        for schema in ["tenant_poc_a", "tenant_poc_b"]:
            await conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {schema}.tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    tenant TEXT NOT NULL
                )
            """))

        # Seed data
        await conn.execute(text("INSERT INTO tenant_poc_a.tasks (title, tenant) VALUES ('Task A1', 'tenant_poc_a'), ('Task A2', 'tenant_poc_a')"))
        await conn.execute(text("INSERT INTO tenant_poc_b.tasks (title, tenant) VALUES ('Task B1', 'tenant_poc_b'), ('Task B2', 'tenant_poc_b')"))

    print("✅ Schemas and data seeded successfully!")
    await engine.dispose()

asyncio.run(seed())