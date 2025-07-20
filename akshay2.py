import sqlite3, json
from datetime import datetime

# Connect to database
cun = sqlite3.connect("my_app.db")
cursor = cun.cursor()

# Create table (fixed typo: YABLE → TABLE)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        task TEXT, 
        day INTEGER PRIMARY KEY CHECK(day BETWEEN 1 AND 31),
        tag TEXT,
        content TEXT,
        timestamp TEXT
    )
""")

# Add a note to the database
def add_notes():
    task = input("Enter the task here: ")
    day = int(input("Enter the day number here: "))
    
    tag_list = input("Enter tags (comma separated): ").split(",") if input("Any tags? (y/n): ").lower() == 'y' else []
    content = input("Enter the content here (short): ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tag_json = json.dumps(tag_list)  # store tags as JSON string
    
    try:
        cursor.execute(
            "INSERT INTO users(task, day, tag, content, timestamp) VALUES (?, ?, ?, ?, ?)",
            (task, day, tag_json, content, timestamp)
        )
        cun.commit()
        print("✅ Note added successfully.")
    except sqlite3.IntegrityError:
        print("❌ A note with this day already exists. Use a different day.")

# Search notes by tag
def search_tags():
    tagger = input("Enter a tag to search: ")

    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()

    found = False
    for row in results:
        tags = json.loads(row[2]) if row[2] else []
        if tagger in tags:
            print("\n--- Matching Note ---")
            print(f"📝 Task: {row[0]}")
            print(f"📅 Day: {row[1]}")
            print(f"🏷️ Tags: {tags}")
            print(f"🧠 Content: {row[3]}")
            print(f"🕒 Timestamp: {row[4]}")
            print("-" * 30)
            found = True

    if not found:
        print("❌ No notes found with this tag.")

# View all notes
def view_notes():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        print("\n📝 Task:", row[0])
        print("📅 Day:", row[1])
        print("🏷️ Tags:", json.loads(row[2]) if row[2] else [])
        print("🧠 Content:", row[3])
        print("🕒 Timestamp:", row[4])
        print("-" * 40)

def edit_note():
    day = int(input("Enter the day number of the note to edit: "))

    cursor.execute("SELECT * FROM users WHERE day = ?", (day,))
    note = cursor.fetchone()

    if note:
        print("\nCurrent values:")
        print(f"Task: {note[0]}")
        print(f"Tags: {json.loads(note[2])}")
        print(f"Content: {note[3]}")

        task = input("New task (leave blank to keep same): ") or note[0]
        tag_input = input("New tags comma-separated (leave blank to keep same): ")
        tag = json.dumps(tag_input.split(",")) if tag_input else note[2]
        content = input("New content (leave blank to keep same): ") or note[3]

        cursor.execute(
            "UPDATE users SET task = ?, tag = ?, content = ? WHERE day = ?",
            (task, tag, content, day)
        )
        cun.commit()
        print("✅ Note updated successfully.")
    else:
        print("❌ No note found for that day.")
def delete_note():
    day = int(input("Enter the day number of the note to delete: "))

    cursor.execute("SELECT * FROM users WHERE day = ?", (day,))
    note = cursor.fetchone()

    if note:
        confirm = input(f"Are you sure you want to delete note from day {day}? (y/n): ").lower()
        if confirm == 'y':
            cursor.execute("DELETE FROM users WHERE day = ?", (day,))
            cun.commit()
            print("🗑️ Note deleted successfully.")
        else:
            print("❌ Deletion cancelled.")
    else:
        print("❌ No note found for that day.")
def main_menu():
    while True:
        print("\n--- Notes App ---")
        print("1. Add Note")
        print("2. View All Notes")
        print("3. Search Notes by Tag")
        print("4. Edit Note")
        print("5. Delete Note")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_notes()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            search_tags()
        elif choice == "4":
            edit_note()
        elif choice == "5":
            delete_note()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❗Invalid option. Try again.")
if __name__ == "__main__":
    main_menu()