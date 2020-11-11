import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
  print('This job is run every three minutes.')

  # Set up Selenium
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

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

  # prepare email address/login
    sender_email = 'princetonnotifier@gmail.com'
    password = 'Notifyme2020!'
    receiver_email = "justincurl13@gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = "[Enrollment Update] {}: {}".format(s_subject, s_course_title)
    message["From"] = sender_email
    message["To"] = receiver_email

  # Create html version of message
    html = """\
    <html>
      <body>
        <h3> Class Information </h3>
    """
    for i in range(len(text)):
      html+= """\
        <ul>
          <li>{}</li>
          <li>{}</li>
          <li>{}</li>
        </ul>
        <br>
      """.format(text[i][0], text[i][1], text[i][2])

    html += """\
      </body>
    </html>
    """

    # Turn html into MIMEText objects
    part1 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

sched.start()