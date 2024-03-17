
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os.path

"""
twilio_num=os.getenv('TWILIO_NUM')
print(twilio_num)
user_num=os.getenv('USER_NUM')
print(user_num)
"""
user_num=os.getenv('USER_NUM')

#Account SID from twilio.com/console
account_sid=os.getenv('TWILIO_ACCOUNT_SID')
 # Your Auth Token from twilio.com/console
auth_token=os.getenv('AUTH_TOKEN')
#Authenticating the twilio messaging API to send messages to the user's number.
client=Client(account_sid,auth_token)



msg= client.messages.create(
                from_='+1 573 577 3756',
                to=user_num,
                body='hii there')
                
print(f'SID: {msg.sid}  Status:  {msg.status}')
