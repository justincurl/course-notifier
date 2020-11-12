import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
from twilio.rest import Client

def notify(SEND_MESSAGE=False):
  # Set up Selenium
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

 # Set-up email sending 
  sender_email = os.environ.get("EMAIL_ADDRESS")
  password = os.environ.get("EMAIL_PASSWORD")
  recipients = ["justincurl13@gmail.com", "jcurl@princeton.edu"]

  # Set-up Twilio Account: the following line needs your Twilio Account SID and Auth Token
  client = Client(os.environ.get("TWILIO_SID"), os.environ.get("TWILIO_AUTH"))

  url_mappings = {
    'POL316': 'https://registrar.princeton.edu/course-offerings/course-details?term=1214&courseid=005300',
    'POL423': 'https://registrar.princeton.edu/course-offerings/course-details?term=1214&courseid=009187',
    'POL563': 'https://registrar.princeton.edu/course-offerings/course-details?term=1214&courseid=005433',
    }
  courses = ['POL316', 'POL423', 'POL563']
  msg_info = ""

  message = MIMEMultipart("alternative")
  msg_subject = "[Enrollment Update] "
  message["From"] = sender_email
  message["To"] = ', '.join(recipients)

  # Loop through courses of interest
  for course in courses:
  # get course and wait for it to load
    driver.get(url_mappings[course])
    time.sleep(2)

  # parse through the page with beautiful soup
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

  # get course title
    s_course_title = soup.find_all("h2", class_="course-title")
    for course in s_course_title:
      try: 
        s_course_title = course.get_text()
        s_course_title = " ".join(s_course_title.split())
      except:
        s_course_title = "title error"

  # get course listing 
    s_subject = soup.find_all("div", class_="subject-associations")
    for course in s_subject:
      try: 
        s_subject = course.get_text()
        s_subject = " ".join(s_subject.split())
      except:
        s_subject = "subject error"

  # add to email subject
    msg_subject += s_subject + " | "
      
  # get enrollment numbers
    s_enrollment = soup.find_all("td", class_="class-enrollment-numbers nowrap")
    s_section = soup.find_all("td", class_="class-section nowrap")
    s_class_number = soup.find_all("td", class_="class-number nowrap")

    text = []
    enrollment = []
    for i in range(len(s_section)):
      enrollment_readable = s_enrollment[i].get_text().split()
      if enrollment_readable[-1] == "limit":
        limit = None
      else:
        limit = int(enrollment_readable[-1])

      enrolled = int(enrollment_readable[1])
      
      enrollment.append((enrolled, limit))

      # check if an email needs to even be send
      if limit != None and enrolled != limit and enrolled > 0:
        print(enrolled, limit)
        print('set to true: ^^')
        SEND_MESSAGE = True
      
      text.append((s_class_number[i], s_section[i]))
  # Create string version of message
    msg_info += "===================\n{}: {}\n===================\n".format(s_subject, s_course_title)
    for i in range(len(text)):
      msg_info += "Class Number: {}\nSection: {}\nEnrolled: {}\nLimit: {}\n".format(text[i][0].get_text(), text[i][1].get_text(), enrollment[i][0], enrollment[i][1])
      msg_info += "\n"
    
  if SEND_MESSAGE:
    print(msg_info)

    message["Subject"] = msg_subject

    # Turn msg_info into MIMEText objects
    part1 = MIMEText(msg_info, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, recipients, message.as_string()
        )
    print('email sent')

    # send text to self
    client.messages.create(to=os.environ.get("PHONE_NUMBER"), 
                          from_=os.environ.get("TWILIO_NUMBER"), 
                          body=msg_info)
    
    print('text sent')
  else:
    print("No Reason to Notify")
  
  driver.quit()

if __name__ == "__main__": 
  notify(True)