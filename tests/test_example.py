# Add your tests here

import pytest

@pytest.mark.asyncio
async def test_crud_example(async_client, prepare_db):
    # --- CREATE ---
    response = await async_client.post(
        "/example/",
        json={"title": "Test", "content": "Initial"}
    )
    assert response.status_code == 201
    data = response.json()
    example_id = data["id"]

    # --- READ ---
    response = await async_client.get(f"/example/{example_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"

    # --- UPDATE ---
    response = await async_client.put(
        f"/example/{example_id}",
        json={"title": "Test Updated", "content": "Changed"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Updated"

    # --- DELETE ---
    response = await async_client.delete(f"/example/{example_id}")
    assert response.status_code == 200

    # --- READ nach DELETE ---
    response = await async_client.get(f"/example/{example_id}")
    assert response.status_code == 404

