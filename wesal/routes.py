from flask import request, jsonify,Response, session
from wesal.utility import db_connection, db_write,generate_salt,generate_hash,db_read,send_login_token,validate_user,decode_jwt_token,generate_verification_code,users,courses,lessons
from . import app

@app.route('/')
@app.route('/user', methods=['GET','POST'])
def user():
    mydb=db_connection()
    my_cursor=mydb.cursor()
    if request.method == 'GET':
        my_cursor.execute("SELECT * FROM User")
        data =my_cursor.fetchall()
        my_cursor.close()
        return jsonify(data)
        
    if request.method=='POST':
        new_username = request.json['username']
        new_phone_number = request.json['phone_number']
        new_email = request.json['email']
        new_image_file = request.json['image_file']
        new_password = request.json['password']
        new_gender = request.json['gender']
        new_birth_date = request.json['birth_date']
        new_user_role = request.json['user_role']
        new_confirm_password = request.json["confirm_password"]
        if new_password == new_confirm_password:
            password_salt = generate_salt()
            password_hash = generate_hash(new_password, password_salt)

            if db_write(
                """INSERT INTO user (username,phone_number,email,image_file,
                password_salt, password_hash,gender,birth_date,user_role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (new_username,new_phone_number,new_email,new_image_file, password_salt, password_hash,
            new_gender,new_birth_date,new_user_role),):
            # Registration Successful
                    return jsonify({"message":"Signed up successfully"})
            else:
            # Registration Failed
                    return jsonify({"message":"Phone number or Email is already exist"})
        else:
            # Registration Failed
            return Response(status=400)

# valid token   
@app.route("/user/<string:token>", methods=["POST"])   
def user_token(token):
        id= decode_jwt_token(token)
        
        if db_read("SELECT * FROM user WHERE id = %s", (id,)):
                return jsonify({"message":"The user has account"})
        else:
                return jsonify({"message":"The user does not have account"})

# update password
@app.route('/password/<int:id>', methods=['PUT'])
def change_password(id):
    if request.method == 'PUT':
        new_password = request.json['password']
        new_confirm_password = request.json["confirm_password"]
        if new_password == new_confirm_password:
            password_salt = generate_salt()
            password_hash = generate_hash(new_password, password_salt)
        else:
            return jsonify({"message":"new_password is not match new_confirm_password"})
        if db_write(
                """UPDATE user SET password_salt = %s, password_hash = %s WHERE id = %s""",
            (password_salt, password_hash,id),):
            #Successful
                    return jsonify({'message': 'Data updated successfully'})
        else:
            #Failed
                    return jsonify({"message":"Something went wrong"})
        
# update username
@app.route('/username/<int:id>', methods=['PUT'])
def change_username(id):
    if request.method == 'PUT':
        new_username = request.json['username']
        if db_write(
                """UPDATE user SET username = %s WHERE id = %s""",
            (new_username,id),):
            #Successful
                    return jsonify({'message': 'Data updated successfully'})
        else:
            #Failed
                    return jsonify({"message":"Something went wrong"})
        


    return jsonify({'error': 'Access token not provided'}), 400
from wesal.sms import send_message

#Register
@app.route("/register", methods=["POST"])
def register_user():
        new_username = request.json['username']
        new_phone_number = request.json['phone_number']
        new_email = request.json['email']
        new_image_file = request.json['image_file']
        new_password = request.json['password']
        new_gender = request.json['gender']
        new_birth_date = request.json['birth_date']
        new_user_role = request.json['user_role']
        new_confirm_password = request.json["confirm_password"]
        if new_password == new_confirm_password:
            password_salt = generate_salt()
            password_hash = generate_hash(new_password, password_salt)
            if db_write(
                """INSERT INTO user (username,phone_number,email,image_file,
                password_salt, password_hash,gender,birth_date,user_role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (new_username,new_phone_number,new_email,new_image_file, password_salt, password_hash,
                new_gender,new_birth_date,new_user_role),):
                    if new_phone_number:
                
                        verification_code= generate_verification_code()
                        if db_write("""INSERT INTO verify (phone_number,code)  VALUES (%s, %s)
                        """, (new_phone_number, verification_code),
                        ):
                            verify=send_message(new_phone_number,verification_code)
                
                            return jsonify({"message":"Verification code will be sent"})
                        
                        else: 
                                return jsonify({"error": "Phone number not provided."}), 400
            
                    else:
                        return jsonify({"error": "Phone number not provided."}), 400   
            # Registration Successful
                    
            else:
                # Registration Failed
                    return jsonify({"message":"Phone number or Email is already exist"})
            
        else:
            # Registration Failed
            return Response(status=400)

#verify
@app.route('/verify/code', methods=['POST'])
def verify_code():
    code = request.json.get('code')
    phone_number = request.json['phone_number']
    if code:
        
        # Retrieve the stored code
        current_code = db_read("SELECT * FROM verify WHERE phone_number = %s", (phone_number,))
        if len(current_code) == 1:
            stored_code = current_code[0]["code"]
            if stored_code and code == stored_code:
            # Code matches
                delete_code=db_write('''DELETE FROM verify WHERE phone_number = %s''', (phone_number,))  # Remove the code from storage
                return jsonify({"message": "Verification successful."}), 200
            else:
                return jsonify({"error": "Invalid verification code."}), 400
        else:
            return jsonify({"error": "Invalid Phone number."}), 400
    else:
        return jsonify({"error": "verification code not provided."}), 400

@app.route('/verify', methods=['POST'])
def verify():
    phone_number = request.json['phone_number']
    if db_read("SELECT * FROM user WHERE phone_number = %s", (phone_number,)):
        verification_code= generate_verification_code()
        if db_write("""INSERT INTO verify (phone_number,code)  VALUES (%s, %s)
                        """, (phone_number, verification_code),
                        ):
                            #verify=send_message(new_phone_number,verification_code)
                
                            return jsonify({"message":"Verification code will be sent"})
                        
        else: 
                            return jsonify({"error": "Phone number not provided."}), 400
    else:
        return jsonify({"error": "Invalid Phone number."}), 400

# Login Route
#USER
@app.route('/login/user', methods=['POST'])
def login_user():
    user_phone_number = request.json["phone_number"]
    user_password = request.json["password"]

    user_token = validate_user(user_phone_number, user_password)
    print(user_token)
    if user_token==1:
        return jsonify({"message":"You do not have an account, please Sign up"})
    elif user_token==2:
        
        return jsonify({"message":"Password is not correct"})
    else:
        session['phone_number'] =user_phone_number
        return jsonify({"jwt_token": user_token})
#ADMIN   
@app.route('/login/admin', methods=['POST'])
def login_admin():
    user_phone_number = request.json["phone_number"]
    user_password = request.json["password"]

    user_token = validate_user(user_phone_number, user_password)
    print(user_token)
    if user_token==1:
        return jsonify({"message":"You do not have an account, please Sign up"})
    elif user_token==2:
        
        return jsonify({"message":"Password is not correct"})
    else:
        session['phone_number'] =user_phone_number
        return jsonify({"jwt_token": user_token})

# logout
from flask_jwt_extended import jwt_required, get_jwt
from wesal.Blocked_list import BLOCKLIST 
@app.route('/logout', methods=['POST'])
def logout():
    if 'phone_number' in session:
        session.pop('phone_number', None)
    return jsonify({'message' : 'You successfully logged out'})
# @app.route('/logout', methods=['DELETE'])
# @jwt_required()
# def logout():
#     jti = get_jwt ()['jti']
#     BLOCKLIST.add(jti)
#     return jsonify({"message": "Successfully logged out"}), 200

#courses:
#create and read
@app.route('/course', methods=['POST','GET'])
def course():
    if request.method == 'GET':
        data = db_read("SELECT * FROM course")
        return jsonify(data)

    if request.method=='POST':
        new_title = request.json['title']
        new_description = request.json['description']
        new_icon = request.json['icon']
        
        if db_write(
                """INSERT INTO course (title,description,icon)
                VALUES (%s, %s, %s)""",
            (new_title,new_description,new_icon),):
            # Successful
                    return jsonify({"message":"New course is add successfully"})
        else:
            # Failed
                    return jsonify({"message":"New course is not add"})
    else:
            # Failed
            return jsonify({"message":"error in connection with database"})  

#delet and update
@app.route('/course/<int:id>', methods=['PUT', 'DELETE'])
def update_course(id):
    if request.method == 'DELETE':
        if db_write('''DELETE FROM course WHERE id = %s''', (id,)):
            return jsonify({'message': 'Course deleted successfully'}), 200
        else:
            return jsonify({'message': 'Failed to delete course'}), 500

    elif request.method == 'PUT':
        new_title = request.json.get('title')
        new_description = request.json.get('description')
        new_icon = request.json.get('icon')

        if not all([new_title, new_description, new_icon]):
            return jsonify({"message": "Missing required fields"}), 400

        if db_write(
            """UPDATE course SET title = %s, description = %s, icon = %s WHERE id = %s""",
            (new_title, new_description, new_icon, id)
        ):
            return jsonify({'message': 'Course updated successfully'}), 200
        else:
            return jsonify({'message': 'Failed to update course'}), 500

    else:
        return jsonify({"message": "Invalid request method"}), 405

import base64
#Lessons:

#Read
@app.route('/lesson/<int:course_id>', methods=['GET'])
def lesson(course_id):
    if request.method == 'GET':
        data = db_read("SELECT * FROM Lesson WHERE course_id = %s", (course_id,))
        
        # Convert binary fields to base64-encoded strings
        for row in data:
            row['video'] = base64.b64encode(row['video']).decode('utf-8') if row['video'] else None
            row['documentation'] = base64.b64encode(row['documentation']).decode('utf-8') if row['documentation'] else None

        return jsonify(data)
    else:
        # Failed
        return jsonify({"message":"ERROR in Course ID"})
        
#Create  
@app.route('/lesson', methods=['POST'])
def create_lesson():
        
    if request.method=='POST':
        new_title = request.json['title']
        new_description = request.json['description']
        new_date_posted = request.json['date_posted']
        new_thumbnail = request.json['thumbnail']
        new_video = request.json['video']
        new_documentation = request.json['documentation']
        new_duration = request.json['duration']
        new_course_id = request.json['course_id']
        new_course_id = int(new_course_id)
        if db_write(
                """INSERT INTO lesson (title,description,date_posted,
                thumbnail,video,documentation,duration,course_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (new_title,new_description,new_date_posted,new_thumbnail,new_video,new_documentation,new_duration,new_course_id),):
            #Successful
                    return jsonify({"message":"New course is add successfully"})
        else:
            # Failed
                    return jsonify({"message":"New course is not add"})
    else:
            # Failed
            return jsonify({"message":"error in connection with database"})  
    
#DELETE and update
@app.route('/lesson/<int:id>', methods=['DELETE', 'PUT'])
def update_lesson(id):
    if request.method == 'DELETE':
        if db_write('''DELETE FROM lesson WHERE id = %s''', (id,)):
            return jsonify({'message': 'Data deleted successfully'})
        else:
            return jsonify({'message': 'Failed to delete data'})
    elif request.method == 'PUT':
        new_title = request.json['title']
        new_description = request.json['description']
        new_date_posted = request.json['date_posted']
        new_thumbnail = request.json['thumbnail']
        new_video = request.json['video']
        new_documentation = request.json['documentation']
        new_duration = request.json['duration']
        new_course_id = request.json['course_id']
        new_course_id = int(new_course_id)
        if db_write(
                """UPDATE lesson SET title = %s, description = %s, date_posted = %s, thumbnail = %s, 
                video = %s, documentation = %s, duration = %s, course_id = %s WHERE id = %s""",
                (new_title, new_description, new_date_posted, new_thumbnail, new_video, new_documentation,
                new_duration, new_course_id, id)):
            return jsonify({'message': 'Data updated successfully'})
        else:
            return jsonify({"message": "Failed to update data"})


#Favorite
#create and read
@app.route('/favorite/<int:user_id>', methods=['GET','POST'])
def favorite(user_id):
    print (user_id)
    if request.method == 'GET':
        data = db_read("SELECT * FROM favorite WHERE user_id = %s", (user_id,))
        return jsonify(data)
    elif request.method=='POST':
        print (user_id)
        new_text = request.json['text']
        new_user_id = user_id
        if db_write(
                """INSERT INTO favorite (text,user_id)
                VALUES (%s, %s)""",
            (new_text,new_user_id),):
            #Successful
                    return jsonify({"message":"Created successfully"})
        else:
            #Failed
                    return jsonify({"message":"You do not have an account, please Sign up"})
        
    else:
            #Failed
            return Response(status=400)

#delete
@app.route('/favorite/<int:id>', methods=['DELETE', 'PUT'])
def delete_favorite(id):
    if request.method == 'PUT':
        new_text = request.json.get('text')

        if not new_text:
            return jsonify({"message": "Missing required fields"}), 400

        if db_write(
            """UPDATE favorite SET text = %s WHERE id = %s""",
            (new_text, id)
        ):
            return jsonify({'message': 'Favorite updated successfully'}), 200
        else:
            return jsonify({'message': 'Failed to update favorite'}), 500

    elif request.method == 'DELETE':
        if db_write('''DELETE FROM favorite WHERE id = %s''', (id,)):
            return jsonify({'message': 'Favorite deleted successfully'}), 200
        else:
            return jsonify({'message': 'Failed to delete favorite'}), 500

    else:
        return jsonify({"message": "Invalid request method"}), 405

