import sqlite3

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create inventory table
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    quantity INTEGER NOT NULL
)
''')

conn.commit()
conn.close()

print(" Database and inventory table created successfully!")
