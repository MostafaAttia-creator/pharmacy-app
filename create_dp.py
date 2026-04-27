import sqlite3

conn = sqlite3.connect(r"E:\my_files\Lectures\Level 2\2nd term\Database\DB_project\pharmacy.db")
cursor = conn.cursor()

# with open(r"E:\my_files\Lectures\Level 2\2nd term\Database\DB_project\schema.sql", "r", encoding="utf-8") as f:
#     sql_script = f.read()

# cursor.executescript(sql_script)



cursor.execute("DELETE FROM Sales")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='Sales'")

cursor.execute("DELETE FROM Customers")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='Customers'")

cursor.execute("DELETE FROM Sale_Items")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='Sale_Items'")

cursor.execute("UPDATE Medicines SET Quantity = 100")


conn.commit()
conn.close()
