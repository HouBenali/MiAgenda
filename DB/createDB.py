import sqlite3
 
# Connecting to sqlite
# connection object
connection_obj = sqlite3.connect('agenda.db')
 
# cursor object
cursor_obj = connection_obj.cursor()
 
# Drop the GEEK table if already exists.
cursor_obj.execute("DROP TABLE IF EXISTS CUSTOMERS")
 
# Creating table
table = """ CREATE TABLE CUSTOMERS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME CHAR(25) NOT NULL,
            SURNAME CHAR(25) NOT NULL,
            PHONE CHAR(25) NOT NULL,
            BIRTHDATE DATE NOT NULL,
            STATUS CHAR(4) NOT NULL
        ); """
 
cursor_obj.execute(table)
 
print("Table is Ready")
 
# Close the connection
connection_obj.close()