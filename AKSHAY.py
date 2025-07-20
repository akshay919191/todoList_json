import sqlite3 , json 
from datetime import datetime

cunn = sqlite3.connect("my_data.db")
cursor = cunn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users
                (task TEXT , 
                id INTEGER PRIMARY KEY , 
                tag TEXT ,
                content TEXT , 
                timestamp TEXT)""")

def add():
    task = input("Enter a task here: ")
    id = int(input("Enter id number:"))
    tag = input("Enter tag: ") if input("is there any tag(y / n):").lower() == "y" else [] 
    content = input("Enter the content of your task here: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tag_json = json.dumps(tag)
    try :
        cursor.execute("INSERT INTO users(task , id , tag , content , timestamp) VALUES ( ? , ? , ? , ? , ?)" , (task , id , tag_json , content , timestamp))
        cunn.commit()
        print("NOTE ADDED✅")
    except sqlite3.IntegrityError:
        print("❌ A note with this day already exists. Use a different day.")

def search():
    tag = input("Enter a tag to search : ")

    cursor.execute("SELECT * FROM users")
    res = cursor.fetchall()
    found = False
    for row in res:
        tags = json.loads(row[2]) if row[2] else []
        if tag in tags:
            print(f"📝task : {row[0]}")
            print(f"📅id : {row[1]}")
            print(f"🏷️tag : {row[2]}")
            print(f"🧠content : {row[3]}")
            print(f"🕒timestamp : {row[4]}")
            found = True
    if not found:
        print("❌we cannot find related to this")
    
def view():
    cursor.execute("SELECT * FROM users")
    res = cursor.fetchall()
    for row in res:
        print(f"📝task : {row[0]}")
        print(f"📅id : {row[1]}")
        print(f"🏷️tag : {json.loads(row[2]) if row[2] else []}")
        print(f"🧠content : {row[3]}")
        print(f"🕒timestamp : {row[4]}")     

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
        cunn.commit()
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
            cunn.commit()
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
            add()
        elif choice == "2":
            view()
        elif choice == "3":
            search()
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