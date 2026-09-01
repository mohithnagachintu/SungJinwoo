from uuid import uuid4


def test_create_task_returns_201(client):
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Write tests"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["status"] == "todo"
    assert body["priority"] == "medium"
    assert "id" in body
    assert "created_at" in body


def test_create_task_requires_title(client):
    response = client.post("/api/v1/tasks", json={})

    assert response.status_code == 422


def test_list_tasks_includes_created_task(client):
    client.post("/api/v1/tasks", json={"title": "Task A"})

    response = client.get("/api/v1/tasks")

    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) >= 1
    assert body["total"] >= 1


def test_get_task_by_id(client):
    created = client.post("/api/v1/tasks", json={"title": "Task B"}).json()

    response = client.get(f"/api/v1/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Task B"


def test_get_unknown_task_returns_404(client):
    response = client.get(f"/api/v1/tasks/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "TASK_NOT_FOUND"


def test_patch_task_updates_fields(client):
    created = client.post("/api/v1/tasks", json={"title": "Task C"}).json()

    response = client.patch(
        f"/api/v1/tasks/{created['id']}",
        json={"status": "done", "priority": "high"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "done"
    assert body["priority"] == "high"
    assert body["title"] == "Task C"


def test_delete_task_returns_204(client):
    created = client.post("/api/v1/tasks", json={"title": "Task D"}).json()

    response = client.delete(f"/api/v1/tasks/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/api/v1/tasks/{created['id']}").status_code == 404


