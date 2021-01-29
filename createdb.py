import sqlite3
db_file = "./state.db"
conn = sqlite3.connect(db_file)

conn.execute('''CREATE TABLE State
         (ID INT PRIMARY KEY     NOT NULL,
         DAY           TEXT    NOT NULL,
         STARTHOUR            INT     NOT NULL,
         ENDHOUR    INT     NOT NULL,
         isOn INT NOT NULL);''')

conn.close()