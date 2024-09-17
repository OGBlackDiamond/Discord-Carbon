import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from email.message import EmailMessage


class GmailUtil: 
    
    SCOPES: list[str]

    # initializes and connects to the google API
    def __init__(self):
        SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())


        # build the service with credentials
        self.service = build("gmail", "v1", credentials=creds)
        


    def send_message(self, recipient: str, user: str, content: str):

        try:

            message = EmailMessage()

            # removes extranious newline characters
            content.replace('\n', '')

            message.set_content(f"Message from Discord by: {user}\n\n{content}\n\n\n\n\n-# Automated messaging from Discord handled by Carbon")

            message["To"] = recipient
            message["From"] = "fyre5480@gmail.com"
            message["Subject"] = "Testing Carbon Discord-to-Email System"


            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
            # pylint: disable=E1101
            draft = (
                self.service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )

        except HttpError as error:
            print(f"An error occurred: {error}")
            draft = None

        return draft
        


