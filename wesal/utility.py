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
mydb=db_connection()
my_cursor=mydb.cursor()
print (mydb)
def db_write(query, params):
    mydb=db_connection()
    my_cursor=mydb.cursor()
    try:
        my_cursor.execute(query, params)
        mydb.commit()
        my_cursor.close()

        return True

    except mysql.connector.Error as e:
        my_cursor.close()
        return False
#  PBKDF2 (Password-Based Key Derivation Function 2) cryptography to generate the password hash.
#To make it even more secure, we will add a random salt to our hash. 
import os

def generate_salt():
    salt = os.urandom(16)
    return salt.hex()

from hashlib import pbkdf2_hmac

def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()

def db_read(query, params=None):
    mydb = db_connection()
    my_cursor = mydb.cursor(dictionary=True)  # Use dictionary cursor

    if params:
        my_cursor.execute(query, params)
    else:
        my_cursor.execute(query)

    entries = my_cursor.fetchall()
    my_cursor.close()

    return entries


# JWT to send as a response to the user when they login.
import jwt
from datetime import datetime, timedelta

def generate_jwt_token(content, expiration_minutes=30 * 24 * 60):
    # Set the expiration time (30 minutes by default)
    expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)

    # Include the expiration time in the payload
    content['exp'] = expiration_time

    # Generate the JWT token
    encoded_content = jwt.encode(content, '6402f96ddc6753297c5d5348641878a9f89a61719b88ee4ef0b1e63972ed624d', algorithm="HS256")
    
    # Return the token
    return encoded_content

def decode_jwt_token(token):
    
    # Decode the token
        decoded_token = jwt.decode(token, '6402f96ddc6753297c5d5348641878a9f89a61719b88ee4ef0b1e63972ed624d', algorithms=["HS256"])
        
        # Extract the ID from the decoded token
        user_id = decoded_token.get('id')

        return user_id
    

def send_login_token(phone_number):
    current_user = db_read("SELECT * FROM user WHERE phone_number = %s", (phone_number,))
    if len(current_user) == 1:
        user_id = current_user[0]["id"]
        jwt_token = generate_jwt_token({"id": user_id})
        return jwt_token
    else:
        return False
def validate_user(phone_number, password):
    current_user = db_read("SELECT * FROM user WHERE phone_number = %s", (phone_number,))
    message=1
    if len(current_user) == 1:
        saved_password_hash = current_user[0]["password_hash"]
        saved_password_salt = current_user[0]["password_salt"]
        entered_password_hash = generate_hash(password, saved_password_salt)


        entered_password_hash2=entered_password_hash[:60]
        if entered_password_hash2 == saved_password_hash:
            user_id = current_user[0]["id"]
            jwt_token = generate_jwt_token({"id": user_id})
            return jwt_token
        else:
            # password is not correct
            message =2
            return message
    else:
        # can not find the user
        return message
    
import random
import string

# Function to generate a random verification code
def generate_verification_code(length=6):
    characters = string.digits  # Use digits for the verification code
    return ''.join(random.choice(characters) for _ in range(length))

users = [
            dict(id=row['id'],username=row['username'],phone_number=row['phone_number'],
                email=row['email'],image_file=row['image_file'],password=row['password'],
                gender=row['gender'],birth_date=row['birth_date'],
                user_role=row['user_role'],last_login=row['last_login'],created_at=row['created_at'])
            for row in my_cursor
        ]
courses= [
            dict(id=row['id'],title=row['title'],description=row['description'],
                icon =row['icon '])
            for row in my_cursor
        ]

lessons= [
            dict(id=row['id'],title=row['title'],description=row['description'],
                duration =row['duration'],date_posted=row['date_posted'],thumbnail=row['thumbnail'],
                videor=row['video'],course_id=row['course_id'],documentation=row['documentation'])
            for row in my_cursor
        ]