import sqlite3

conn = sqlite3.connect('my_quotes.db')

curr = conn.cursor()

# curr.execute("""create table quotes_tb(
#                 title text,
#                 author text,
#                 tag text
#                 )""")

curr.execute("""insert into quotes_tb values ('Python is awesome!', 'Md. Kamrul', 'test,test2') """)
conn.commit()
conn.close()