# test_sqlalchemy_schema.py
import asyncio
import httpx

async def test_tenant_isolation():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        
        # Test tenant_poc_a
        r_a = await client.get("/tasks", headers={"x-tenant-slug": "tenant_poc_a"})
        print("Tenant A tasks:", r_a.json())
        assert all(t["tenant"] == "tenant_poc_a" for t in r_a.json()), "❌ Tenant A isolation failed!"
        print("✅ Tenant A isolated correctly")

        # Test tenant_poc_b
        r_b = await client.get("/tasks", headers={"x-tenant-slug": "tenant_poc_b"})
        print("Tenant B tasks:", r_b.json())
        assert all(t["tenant"] == "tenant_poc_b" for t in r_b.json()), "❌ Tenant B isolation failed!"
        print("✅ Tenant B isolated correctly")

        print("\n🎉 Tenant isolation test PASSED!")

asyncio.run(test_tenant_isolation())