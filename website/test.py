import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

desc_table = "CREATE table candidateTable (id int, email text, manifesto text)"
user = (1, "hi@gmail.com", "na me be that")
query = "INSERT INTO candidateTable VALUES(?,?,?)"

cursor.execute(query, user)

select_query = "SELECT * FROM candidateT"

for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()