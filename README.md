# Nexsoverse - Schema-Based Multi-Tenancy POC

This repository contains a Proof of Concept (POC) for building a multi-tenant backend using **FastAPI** and **SQLAlchemy (async)** with PostgreSQL. Multi-tenancy is achieved by utilizing PostgreSQL schemas, providing complete data isolation for each tenant within a single shared database.

## Features

- **FastAPI** for high-performance, asynchronous REST API endpoints.
- **SQLAlchemy (Async)** with **asyncpg** for robust, non-blocking database interactions.
- **PostgreSQL Schemas**: Isolates tenant data by dynamically switching the `search_path` per HTTP request.
- **Data Seeding**: An included script to easily set up tenant schemas, tables, and mock data.
- **Isolation Testing**: A simple async test script using `httpx` to verify that cross-tenant data boundaries are strictly enforced.

## Project Structure

- `main.py`: The FastAPI application containing the API routes and the middleware/logic for dynamic schema switching based on the `x-tenant-slug` HTTP header.
- `seed.py`: Database seeding script. It creates schemas (e.g., `tenant_poc_a`, `tenant_poc_b`), creates the necessary shared tables, and inserts initial test data for each tenant.
- `test_sqlalchemy_schema.py`: Test script that validates the tenant isolation of the `/tasks` endpoint by verifying the returned records.
- `requirements`: The list of Python dependencies required to run the project.

## Prerequisites

- Python 3.8+
- A running PostgreSQL database instance

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd nexsoverse
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements
   ```

4. **Configure Environment Variables:**
   Ensure you have a `.env` file in the root directory with your PostgreSQL connection string:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/your_database_name
   ```

## Usage

1. **Seed the database:**
   Run the seed script to create the necessary schemas and insert mock data.
   ```bash
   python seed.py
   ```

2. **Run the FastAPI server:**
   Start the application locally using Uvicorn.
   ```bash
   uvicorn main:app --reload
   ```

3. **Test the API endpoints:**
   Once the server is running, you can retrieve tenant-specific data by providing the right headers.

   Example for `tenant_poc_a`:
   ```bash
   curl -H "x-tenant-slug: tenant_poc_a" http://127.0.0.1:8000/tasks
   ```

   Example for `tenant_poc_b`:
   ```bash
   curl -H "x-tenant-slug: tenant_poc_b" http://127.0.0.1:8000/tasks
   ```

## Testing Isolation

A test script is included to quickly verify that data isolation across PostgreSQL schemas is working as intended. Ensure the FastAPI server is running (`uvicorn main:app`) before executing the test script:

```bash
python test_sqlalchemy_schema.py
```
