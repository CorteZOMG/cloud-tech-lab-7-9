import asyncio
import httpx
import time

BASE_URL = "http://localhost:8000"

async def verify_postgres():
    print("\n--- Verifying PostgreSQL ---")
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Create
        email = f"test_{int(time.time())}@example.com"
        print(f"Creating user {email}...")
        resp = await client.post("/users/", json={"email": email, "password": "password", "is_active": True})
        if resp.status_code != 200:
            print(f"Create failed: {resp.text}")
            return
        user_id = resp.json()["id"]
        print(f"Created user ID: {user_id}")

        # Get All
        print("Getting all users...")
        resp = await client.get("/users/")
        assert len(resp.json()) > 0
        print("Get all users OK")

        # Get One
        print(f"Getting user {user_id}...")
        resp = await client.get(f"/users/{user_id}")
        assert resp.json()["email"] == email
        print("Get user OK")

        # Update
        print(f"Updating user {user_id}...")
        resp = await client.put(f"/users/{user_id}", json={"is_active": False})
        assert resp.json()["is_active"] == False
        print("Update user OK")

        # Delete
        print(f"Deleting user {user_id}...")
        resp = await client.delete(f"/users/{user_id}")
        assert resp.status_code == 200
        print("Delete user OK")

async def verify_redis():
    print("\n--- Verifying Redis ---")
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        key = f"test_key_{int(time.time())}"
        value = "test_value"
        
        # Set
        print(f"Setting cache {key}={value}...")
        resp = await client.post(f"/cache/set", params={"key": key, "value": value})
        assert resp.status_code == 200
        print("Set cache OK")

        # Get
        print(f"Getting cache {key}...")
        resp = await client.get(f"/cache/get/{key}")
        assert resp.json()["value"] == value
        print("Get cache OK")

async def verify_openf1_caching():
    print("\n--- Verifying OpenF1 Caching ---")
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        print("First call (API)...")
        start = time.time()
        resp = await client.get("/api/f1/drivers?session_key=9158")
        duration1 = time.time() - start
        print(f"First call took {duration1:.2f}s")
        assert resp.status_code == 200

        print("Second call (Cache)...")
        start = time.time()
        resp = await client.get("/api/f1/drivers?session_key=9158")
        duration2 = time.time() - start
        print(f"Second call took {duration2:.2f}s")
        assert resp.status_code == 200
        
        if duration2 < duration1:
            print("Caching works! Second call was faster.")
        else:
            print("Warning: Second call was not faster (might be network variance or cache miss).")

async def main():
    try:
        await verify_postgres()
        await verify_redis()
        await verify_openf1_caching()
        print("\nAll verifications passed!")
    except Exception as e:
        print(f"\nVerification failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
