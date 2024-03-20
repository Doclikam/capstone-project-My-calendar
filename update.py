import datetime as dt 
import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests


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

            #storing the credentials in pickle
            pickle.dump(credentials, open("token.pkl", "wb"))
            credentials = pickle.load(open("token.pkl", "rb"))

        with open('token.json','w') as token:
                token.write(creds.to_json())


    try:
        #building a service object
        service=build('calendar', 'v3', credentials=creds)
    


        """
        creating an event
        summary; title of the event, start:  end: timezone: event_id: description: location:  recurrrence
        color_id: visibility: attendees: attachments:  conference_solution: default reminders: minutes_before_popup_reminder
        minutes_before_email_reminder: guests_can_invite_others: guests_can_modify:  guests_can_see_other_guests
        transparency:  _creator: _organizer:  _created: _updated: recurring_event_id

        """
        event = {
            'summary': 'My Special Event',
            'location': 'Art Caffe',
            'description': 'This is a book reading event',
            'color': 4, 
            'start':{
                'dateTime': '2024-03-28T06:00:00+03:00',
                'timeZone': 'Europe/Vienna'
            },
            'end':{
                'dateTime': '2024-03-28T12:00:00+03:00',
                'timeZone': 'Europe/Vienna'
            },
            'recurrence': None,
            'attendees': {'email': 'likamwambui28@gmail.com'}
            }

        event=service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created {event.get('htmllink')}')



    except HttpError as error:
        print(f'An error occured!: {error}')


if __name__ == '__main__':
    main()


    
