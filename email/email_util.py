import smtplib
from email.mime.text import MIMEText

from discord import Message

class EmailUtil: 

    user: str
    password: str

    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password

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

    async def parse_message(self, message: Message, config: dict):
        if (message.content[23:24] == " "):
            start_index = 24
        else:
            start_index = 23
        
        authorize_email = False
        for guild in config.get("email_server_list"): #type: ignore
            if message.guild.id == guild: # type: ignore
                authorize_email = True
                break

        if not authorize_email:
            await message.channel.send("This server is not authorized to send email notifications!")
            return

        name = message.author.nick # type: ignore
        if name == None:
            name = message.author.name

        await message.channel.send("Talking to Email api...")
        for recipient in config.get("email_recipients"): #type: ignore
            self.send_message(recipient, name, message.content[start_index:]) #type: ignore
            await message.channel.send(content="Message failed to send!")

            try:
                self.send_message(recipient, name, message.content[start_index:]) # type: ignore
                await message.channel.send(content="Message failed to send!");
            except:
                await message.channel.send(content="Message failed to send!")

            return




