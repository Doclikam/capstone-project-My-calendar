             
import datetime as dt 
import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
from flask import Flask
from datetime import datetime, timedelta

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse




#Account SID from twilio.com/console
account_sid=os.getenv('TWILIO_ACCOUNT_SID')
 # Your Auth Token from twilio.com/console
auth_token=os.getenv('AUTH_TOKEN')
#Authenticating the twilio messaging API to send messages to the user's number.
client=Client(account_sid,auth_token)
twilio_num=os.getenv('TWILIO_NUM')
user_num=os.getenv('USER_NUM')


#defining the scope that will allow read and write events in the calendar
SCOPES=["https://www.googleapis.com/auth/calendar"]

def main():
    creds=None
    #the token will be loaded from the credentials file
    if os.path.exists('token.json'):
        creds=Credentials.from_authorized_user_file("token.json")
    #if the credentials are not valid or present
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            #allowing the user to sign into their accounts
            flow=InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds=flow.run_local_server(port=0)

            

        with open('token.json','w') as token:
                token.write(creds.to_json())

def build():
        #building a service object
        service=build('calendar', 'v3', credentials=creds)

   


def now():
    #get the value timeMin and timeMax to the current date
    print(datetime.date.day)

    #get the time the function is called timeMin
    now = dt.datetime.utcnow().isoformat() + 'Z'
    print(now)
    return now

try: 
    def tommorow():
        #get the the time 24 hours from now
        tomorrow = (dt.datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'
        print(tomorrow)
        return tommorow


    
    #get all the vent scheduled within 24 hours
    events_result = service.events().list(
            calendarId='primary',
            timeMin=now ,
            timeMax = tomorrow,
            singleEvents=True,
            orderBy='startTime').execute()

    events = events_result.get('items', [])
    event_plans=[]
    if events:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            #print(start, event['summary'])
            event_plans.append(start)


            msg= Client.messages.create(
                    to=user_num,
                    from_=twilio_num,
                    body=event_plans + event['summary'])
            print(msg.sid)
    

    else:

        
        print('No events in your calendar')


    #automating the messages at a certain time everyday
    
    schedules=schedule.every().day.at('12:30').do(send_schedule)
        


except HttpError as error:
        print(f'An error occured!: {error}')

if __name__ == '__main__':
    main()


    

        

    