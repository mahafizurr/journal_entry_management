from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the database
def initialize_db():
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS journal_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Route: Homepage (List all entries)
@app.route("/")
def index():
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, timestamp FROM journal_entries")
    entries = cursor.fetchall()
    conn.close()
    return render_template("index.html", entries=entries)

# Route: Add new entry
@app.route("/add", methods=["GET", "POST"])
def add_entry():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect("journal.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO journal_entries (title, content, timestamp) VALUES (?, ?, ?)", 
                       (title, content, timestamp))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add_entry.html")

# Route: View details of an entry
@app.route("/entry/<int:entry_id>")
def view_entry(entry_id):
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM journal_entries WHERE id = ?", (entry_id,))
    entry = cursor.fetchone()
    conn.close()
    return render_template("view_entry.html", entry=entry)

# Route: Edit an entry
@app.route("/edit/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()

    if request.method == "POST":
        new_title = request.form["title"]
        new_content = request.form["content"]
        cursor.execute("UPDATE journal_entries SET title = ?, content = ? WHERE id = ?", 
                       (new_title, new_content, entry_id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM journal_entries WHERE id = ?", (entry_id,))
    entry = cursor.fetchone()
    conn.close()
    return render_template("edit_entry.html", entry=entry)

# Route: Delete an entry
@app.route("/delete/<int:entry_id>")
def delete_entry(entry_id):
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM journal_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Run the application
if __name__ == "__main__":
    initialize_db()  # Initialize database only once
    app.run(host="0.0.0.0", port=5000)  # Bind to 0.0.0.0 for public access

