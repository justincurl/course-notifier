import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
from twilio.rest import Client

def notify():
  # Set up Selenium
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

 # Set-up email account
  sender_email = 'princetonnotifier@gmail.com'
  password = 'Notifyme2020!'
  receiver_email = ["justincurl13@gmail.com", "jcurl@princeton.edu"]

  # Set-up Twilio Account: the following line needs your Twilio Account SID and Auth Token
  client = Client("AC8ccc3ec03758febba17614ee5aecdeb1", "97c687fbe1e5c42ba09f99ffc3557241")

  url_mappings = {
    'POL316': 'https://registrar.princeton.edu/course-offerings/course-details?term=1214&courseid=005300',
    'POL423': 'https://registrar.princeton.edu/course-offerings/course-details?term=1214&courseid=009187',
    'POL563': 'https://registrar.princeton.edu/course-offerings/course-details?term=1214&courseid=005433',
    }
  courses = ['POL316', 'POL423', 'POL563']

  # Loop through courses of interest
  for course in courses:
  # get course and wait for it to load
    driver.get(url_mappings[course])
    time.sleep(2)

  # parse through the page with beautiful soup
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    print("============ SOUP ==========")
    print(soup.prettify())

  # get course title for email subject
    s_course_title = soup.find_all("h2", class_="course-title")
    for course in s_course_title:
      try: 
        s_course_title = course.get_text()
      except:
        s_course_title = "error"

  # get course listing for email subject
    s_subject = soup.find_all("div", class_="subject-associations")
    for course in s_subject:
      try: 
        s_subject = course.get_text()
      except:
        s_subject = "error"
      
  # get enrollment numbers
    s_enrollment = soup.find_all("td", class_="class-enrollment-numbers nowrap")
    s_section = soup.find_all("td", class_="class-section nowrap")
    s_class_number = soup.find_all("td", class_="class-number nowrap")

    text = []
    for i in range(len(s_section)):
      text.append((s_class_number[i], s_section[i], s_enrollment[i]))

    message = MIMEMultipart("alternative")
    message["Subject"] = "[Enrollment Update] {}: {}".format(s_subject, s_course_title)
    message["From"] = sender_email
    message["To"] = receiver_email.join(',')

  # Create html version of message
    text = """\
      Class Information:
    """
    for i in range(len(text)):
      text+= """\
        Class Number: {} \n
        Section: {} \n
        Enrollment: {} \n
      """.format(text[i][0], text[i][1], text[i][2])

    # Turn html into MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    # send text to self
    client.messages.create(to="+16465491230", 
                          from_="+12184768626", 
                          body=text)