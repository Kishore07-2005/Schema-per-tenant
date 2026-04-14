🏗️ Schema-per-Tenant PoC — Multi-Tenant Architecture
A Proof of Concept validating PostgreSQL schema-per-tenant isolation using FastAPI, SQLAlchemy Async, and asyncpg.
---
📌 What This Project Does
This PoC validates that `SET search_path` works reliably with SQLAlchemy async sessions to isolate data between tenants in a multi-tenant application.
Each tenant gets their own PostgreSQL schema (like a folder inside the database). When a request comes in, the server switches to that tenant's schema — so Tenant A can never see Tenant B's data.
---
🧪 Test Results
Test	Description	Status
Test 1	SQLAlchemy Async session isolation	✅ PASSED
Test 2	LangChain PGVector tenant isolation	🔄 In Progress
Test 3	LangGraph PostgresSaver isolation	🔄 In Progress
Test 4	Connection pool search_path leak test	🔄 In Progress
---
🗂️ Project Structure
```
nexsoverse/
│
├── .env                  ← secret credentials (never uploaded)
├── .env.example          ← template for environment variables
├── .gitignore            ← files ignored by git
├── seed.py               ← creates schemas and seeds test data
├── main.py               ← FastAPI server (tenant-aware API)
└── test_sqlalchemy_schema.py  ← validates tenant isolation
```
---
⚙️ How It Works
```
seed.py        →   Creates tenant_poc_a and tenant_poc_b schemas in PostgreSQL
main.py        →   FastAPI server that reads X-Tenant-Slug header and sets search_path
test file      →   Sends requests to the server and verifies data isolation
```
The Key Line
```python
await session.execute(text(f"SET search_path TO {tenant_slug}, public"))
```
This single line tells PostgreSQL to only look inside that tenant's schema folder — achieving complete data isolation.
---
🚀 Getting Started
1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/nexsoverse-multitenant-poc.git
cd nexsoverse-multitenant-poc
```
2. Install dependencies
```bash
pip install fastapi sqlalchemy asyncpg uvicorn httpx python-dotenv pytest pytest-asyncio
```
3. Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your actual database credentials.
4. Set up the database
Make sure PostgreSQL is running, then run:
```bash
python seed.py
```
5. Start the API server
```bash
python -m uvicorn main:app --reload
```
6. Run the tests
Open a second terminal and run:
```bash
python test_sqlalchemy_schema.py
```
---
🔐 Environment Variables
Create a `.env` file based on `.env.example`:
```env
DATABASE_URL=postgresql+asyncpg://your_username:your_password@localhost/taskflow
```
---
📦 Dependencies
Package	Purpose
`fastapi`	API framework
`sqlalchemy`	Database ORM and query builder
`asyncpg`	Async PostgreSQL driver
`uvicorn`	ASGI web server
`httpx`	HTTP client for testing
`python-dotenv`	Load environment variables from .env
---
🧠 Concepts Used
Multi-tenancy — Multiple clients sharing one database securely
PostgreSQL Schemas — Isolated "folders" inside a database per tenant
SET search_path — Dynamically switches which schema PostgreSQL looks at
Async SQLAlchemy — Non-blocking database queries
FastAPI — Modern Python API framework
---
👨‍💻 Author
Kishore Kumar
Part of the Nexsoverse backend team — Schema-per-Tenant PoC Sprint
