import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

driver.get('https://registrar.princeton.edu/course-offerings/course-details?term=1214&courseid=005300')

driver.save_screenshot('screenshot.png')

page = driver.page_source

print(page)

soup = BeautifulSoup(page, 'html.parser')

results = soup.find(id='course-details')
  
print(results)

# # sections = results.find_all('td', class_='class-enrollment-numbers nowrap')
# # for section in sections:
# #   print(section.contents[2].value)
# #   # print(section.prettify())

sender_email = 'princetonnotifier@gmail.com'
password = 'Notifyme2020!'
receiver_email = "justincurl13@gmail.com"

message = MIMEMultipart("alternative")
message["Subject"] = "%s Course Notification".format("Pol 315")
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )