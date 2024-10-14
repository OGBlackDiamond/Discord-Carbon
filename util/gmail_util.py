import os.path

import json

import smtplib
from email.mime.text import MIMEText

class GmailUtil: 

    user: str
    password: str
    to: str

    def __init__(self):
        with open("config.json", "r") as file:
            config = json.loads(file.read())

            self.user = config["from"]
            self.password = config["password"]
            self.to = config["to"]
    
    def send_message(self, recipient: str, user: str, content: str):
        # Create a MIMEText object with the body of the email.
        msg = MIMEText(content)
        # Set the subject of the email.
        msg['Subject'] = f"Message from Discord by {user}" 
        # Set the sender's email.
        msg['From'] = self.user 
        # Join the list of recipients into a single string separated by commas.
        msg['To'] = recipient
       
        # Connect to Gmail's SMTP server using SSL.
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            # Login to the SMTP server using the sender's credentials.
            smtp_server.login(self.user, self.password)             
            # Send the email. The sendmail function requires the sender's email, the list of recipients, and the email message as a string.
            smtp_server.sendmail(self.user, recipient, msg.as_string())
        # Print a message to console after successfully sending the email.
        print("Message sent!")

