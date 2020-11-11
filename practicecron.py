import sendgrid
import string
from credentials import username, password
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Your From email address
fromEmail = "justincurl13@gmail.com"
# Recipient
toEmail = "jcurl@princeton.edu"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Testing Message"
msg['From'] = fromEmail
msg['To'] = toEmail

# Create the body of the message (a plain-text and an HTML version).
# text is your plain-text email
# html is your html version of the email
# if the reciever is able to view html emails then only the html
# email will be displayed
text = "Hi!\nHow are you?\n"


html = """\n
<html>
  <head></head>
  <body>
    Hi!<br>
       How are you?<p>
     Weather.com says: It is 32 now in South San Francisco. <p>
     Yahoo says: It is 32 F now in South San Francisco. <p>
     
     smooches, <br>
    the white rabbit
  </body>
</html>
 """

# Login credentials - update them with your own!

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
msg.attach(part1)
msg.attach(part2)

# Open a connection to the SendGrid mail server
s = smtplib.SMTP('smtp.sendgrid.net', 587)

# Authenticate
s.login(username, password)

# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(fromEmail, toEmail, msg.as_string())

s.quit()