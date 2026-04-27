import sqlite3

# conn = sqlite3.connect(r"E:\my_files\Lectures\Level 2\2nd term\Database\DB_project\pharmacy.db")
# cursor = conn.cursor()

# with open(r"E:\my_files\Lectures\Level 2\2nd term\Database\DB_project\schema.sql", "r", encoding="utf-8") as f:
#     sql_script = f.read()

# cursor.executescript(sql_script)

# conn.commit()
# conn.close()

conn = sqlite3.connect(r"E:\my_files\Lectures\Level 2\2nd term\Database\DB_project\pharmacy.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM Sales")
cursor.execute("DELETE FROM Sale_Details")

cursor.execute("DELETE FROM sqlite_sequence WHERE name='Sales'")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='Sale_Details'")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    Customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT
)
""")

cursor.execute("DELETE FROM Customers")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='Customers'")

cursor.execute("""ALTER TABLE Customers
               ADD COLUMN cart TEXT""")

conn.commit()
conn.close()

