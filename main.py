from fastapi import FastAPI, Header, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

async def get_session_for_tenant(tenant_slug: str) -> AsyncSession:
    engine = create_async_engine(DB_URL, echo=True)
    async with AsyncSession(engine) as session:
        await session.execute(text(f"SET search_path TO {tenant_slug}, public"))
        return session

@app.get("/tasks")
async def get_tasks(x_tenant_slug: str = Header(...)):
    valid_tenants = ["tenant_poc_a", "tenant_poc_b"]
    if x_tenant_slug not in valid_tenants:
        raise HTTPException(status_code=400, detail="Invalid tenant")

    engine = create_async_engine(DB_URL, echo=True)
    async with AsyncSession(engine) as session:
        await session.execute(text(f"SET search_path TO {x_tenant_slug}, public"))
        result = await session.execute(text("SELECT * FROM tasks"))
        rows = result.fetchall()
        return [{"id": r[0], "title": r[1], "tenant": r[2]} for r in rows]