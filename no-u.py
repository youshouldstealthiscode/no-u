import os
import random
import time
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
import schedule

# Load the environment variables from the .env file
load_dotenv()

def get_credentials(scopes):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def create_spammers_group(creds):
    try:
        service = build('people', 'v1', credentials=creds, static_discovery=False)

        group_name = 'spammers'
        group_metadata = {'groupMetadata': {'deleted': False}, 'contactGroup': {'name': group_name}}
        contact_group = service.contactGroups().create(body=group_metadata).execute()

        print(f"Created contact group '{group_name}' with resource name '{contact_group.get('resourceName')}'")

    except HttpError as error:
        print(f"An error occurred: {error}")

def get_spammers_emails(creds):
    people_api = build('people', 'v1', credentials=creds)

    contact_groups = people_api.contactGroups().list().execute()
    spammers_group = next((group for group in contact_groups['contactGroups'] if group['name'] == 'spammers'), None)

    if not spammers_group:
        print("No 'spammers' contact group found.")
        return []

    spammers_contacts = people_api.people().connections().list(resourceName='people/me', pageSize=100, groupResourceName=spammers_group['resourceName'], personFields='emailAddresses').execute()
    spammers_emails = [email['value'] for contact in spammers_contacts['connections'] for email in contact['emailAddresses']]

    return spammers_emails

def send_email(gmail_api, to, subject, body):
    sender_email = os.getenv('GMAIL_ADDRESS')
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    send_message = (gmail_api.users().messages().send(userId="me", body=create_message).execute())
    print(F'sent message to {to} Message Id: {send_message["id"]}')

def send_random_email(gmail_api, recipients, subjects, messages):
    recipient = random.choice(recipients)
    subject = random.choice(subjects)
    message = random.choice(messages)
    send_email(gmail_api, recipient, subject, message)

def random_schedule(gmail_api, recipients, subjects, messages):
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day1 = random.choice(days)
    day2 = random.choice(days)
    while day1 == day2:
        day2 = random.choice(days)

    hour1 = random.randint(0, 23)
    hour2 = random.randint(0, 23)
    minute1 = random.randint(0, 59)
    minute2 = random.randint(0, 59)

    schedule.every().at(f"{day1} {hour1}:{minute1}").do(send_random_email, gmail_api, recipients, subjects, messages)
    schedule.every().at(f"{day2} {hour2}:{minute2}").do(send_random_email, gmail_api, recipients, subjects, messages)

def main():
    scopes = ['https://www.googleapis.com/auth/contacts', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/contacts.readonly']
    creds = get_credentials(scopes)

    create_spammers_group(creds)
    recipients = get_spammers_emails(creds)

    gmail_api = build('gmail', 'v1', credentials=creds)

    subjects = ['Subject 1', 'Subject 2', 'Subject 3']
    messages = ['Message content 1', 'Message content 2', 'Message content 3']

    random_schedule(gmail_api, recipients, subjects, messages)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    main()

