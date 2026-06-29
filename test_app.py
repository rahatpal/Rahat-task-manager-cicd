import pytest
import sqlite3
import app as task_app

@pytest.fixture
def client():
    task_app.app.config["TESTING"] = True
    task_app.DB_PATH = "test_tasks.db"
    conn = sqlite3.connect(task_app.DB_PATH)
    conn.execute("DROP TABLE IF EXISTS tasks")
    conn.close()
    task_app.init_db()
    with task_app.app.test_client() as c:
        yield c
    conn = sqlite3.connect(task_app.DB_PATH)
    conn.execute("DROP TABLE IF EXISTS tasks")
    conn.close()
    task_app.app.config["TESTING"] = False

def test_home_page_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200

def test_home_page_shows_empty_message(client):
    response = client.get("/")
    assert b"No tasks yet" in response.data

def test_add_task(client):
    response = client.post("/add", data={"title": "Buy groceries", "description": "Milk and eggs"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Buy groceries" in response.data

def test_add_task_page_loads(client):
    response = client.get("/add")
    assert response.status_code == 200
    assert b"Add Task" in response.data

def test_toggle_task_status(client):
    client.post("/add", data={"title": "Togglable task"}, follow_redirects=True)
    response = client.get("/toggle/1", follow_redirects=True)
    assert response.status_code == 200

def test_delete_task(client):
    client.post("/add", data={"title": "Delete me"}, follow_redirects=True)
    conn = sqlite3.connect("test_tasks.db")
    row = conn.execute("SELECT id FROM tasks WHERE title = ?", ("Delete me",)).fetchone()
    conn.close()
    assert row is not None
    task_id = row[0]
    response = client.get(f"/delete/{task_id}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Delete me" not in response.data

def test_multiple_tasks(client):
    client.post("/add", data={"title": "Task A"}, follow_redirects=True)
    client.post("/add", data={"title": "Task B"}, follow_redirects=True)
    response = client.get("/")
    assert b"Task A" in response.data
    assert b"Task B" in response.data
