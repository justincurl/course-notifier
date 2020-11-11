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

url_mappings = {
  'POL316': 'https://registrar.princeton.edu/course-offerings/course-details?term=1214&courseid=005300',
  'POL423': 'https://registrar.princeton.edu/course-offerings/course-details?term=1214&courseid=009187',
  'POL563': 'https://registrar.princeton.edu/course-offerings/course-details?term=1214&courseid=005433',
  }
courses = ['POL316', 'POL423', 'POL563']
for course in courses:
  driver.get(url_mappings[course])

  page = driver.page_source

  soup = BeautifulSoup(page, 'html.parser')

  print("============ SOUP ==========")
  print(soup.prettify())

  results = soup.find(id='course-details')

  s_course_title = soup.find_all("h2", class_="course-title")
  s_subject = soup.find_all("div", class_="subject-associations")
  s_enrollment = soup.find_all("td", class_="class-enrollment-numbers nowrap")
  s_section = soup.find_all("td", class_="class-section nowrap")
  s_class_number = soup.find_all("td", class_="class-number nowrap")

  text = []
  for i in range(len(s_section)):
    text.append((s_class_number[i], s_section[i], s_enrollment[i]))

  sender_email = 'princetonnotifier@gmail.com'
  password = 'Notifyme2020!'
  receiver_email = "justincurl13@gmail.com"

  message = MIMEMultipart("alternative")
  message["Subject"] = "[Enrollment Update] {}: {}".format(s_subject, s_course_title)
  message["From"] = sender_email
  message["To"] = receiver_email

  # Create the plain-text and HTML version of your message

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

  # Turn these into plain/html MIMEText objects
  part1 = MIMEText(html, "html")

  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(part1)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(
          sender_email, receiver_email, message.as_string()
      )