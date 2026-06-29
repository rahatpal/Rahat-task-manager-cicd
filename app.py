import sqlite3
import os

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
"""Flask task manager application with SQLite backend."""
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")
DB_PATH = "tasks.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )


init_db()


@app.route("/")
def index():
    with sqlite3.connect(DB_PATH) as conn:
        tasks = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description", "")
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)",
                (title, description),
            )
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        task = conn.execute(
            "SELECT status FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if task:
            new_status = "done" if task[0] == "pending" else "pending"
            conn.execute(
                "UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id)
            )
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
