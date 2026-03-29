import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT
)
""")
conn.commit()


def add_task(user_id, text):
    cursor.execute(
        "INSERT INTO tasks (user_id, text) VALUES (?, ?)",
        (user_id, text)
    )
    conn.commit()

def update_task(task_id, user_id, new_text):
    cursor.execute(
        "UPDATE tasks SET text = ? WHERE id = ? AND user_id = ?",
        (new_text, task_id, user_id)
    )
    conn.commit()
    
def get_tasks(user_id):
    cursor.execute(
        "SELECT id, text FROM tasks WHERE user_id = ?",
        (user_id,)
    )
    return cursor.fetchall()

def delete_task(task_id, user_id):
    cursor.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, user_id)
    )
    conn.commit()