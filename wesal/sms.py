# import sys
# sys.path.append('E:\FCAI\Graduation project\Sign language - Copy\myEnv\Lib\site-packages')
from twilio.rest import Client
def send_message(Phone_number,code):
# Your Account SID and Auth Token from console.twilio.com
    account_sid = "AC7c6c96e5267f800c88ddba62dbf221ae"
    auth_token  = "ef37fb8b687033245aca80bdfd6fe686"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=Phone_number,
        from_="+12513135099",
        body="Your verification code is:" +code )
    return 1