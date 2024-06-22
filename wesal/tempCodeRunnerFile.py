import mysql.connector

def db_connection():
    mydb=None
    try:
        mydb= mysql.connector.connect(
            host="sql111.infinityfree.com",
            database='if0_36769195_wesal',
            user="if0_36769195",
            passwd="N5cSco3Ah78Y9")
    except mysql.Error as e:
        print (e)
    return mydb