import sqlite3

# Connect to your IoTGuard database
conn = sqlite3.connect("iotguard.db")
c = conn.cursor()

# Fetch all user data
c.execute("SELECT * FROM users")
rows = c.fetchall()

# Display the data
print("=== USERS TABLE ===")
for row in rows:
    print(row)

conn.close()