# course-notifier

Python application that uses Selenium and BeautifulSoup to scrape Princeton Course offerings to track course enrollment in specified courses. 

If there is an opening in a specified course, the application will use Twilio's sms and gmail's SMTP functionality to text and email me. 

Application is hosted on heroku, using APScheduler to automatically re-check course offerings for updates every three minutes.
