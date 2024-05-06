import mysql.connector

def db_connection():
    mydb=None
    try:
        mydb= mysql.connector.connect(
            host="localhost",
            database='asl_wesal',
            user="root",
            passwd="password123")
    except mysql.Error as e:
        print (e)
    return mydb
mydb=db_connection()
my_cursor=mydb.cursor()
print (mydb)