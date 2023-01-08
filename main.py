import time
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
import smtplib

URL = "https://www.skidrowreloaded.com/"

response = requests.get(URL)
website = response.text

email_from = "edernonato47teste@hotmail.com"
password = "Eder@teste321"
SMTP = "smtp-mail.outlook.com"
PORT = 587

connection = smtplib.SMTP(SMTP, PORT)
connection.starttls()
connection.login(user=email_from, password=password)
email_to = "edernonato@outlook.com"

soup = BeautifulSoup(website, "html.parser")
last_game = soup.find(name="h2").text
last_game_link = soup.find(name="h2").a.get('href')
image_tag = soup.find(name="img", class_="aligncenter")
t = time.localtime()

image_link = image_tag.get("data-lazy-src")
html_start = f'''
    <html>
        <body>
            <h4>New Cracked Game: {last_game} - {time.strftime("%H:%M:%S", t)}</h2>
            <a href="{last_game_link}">{last_game}</a>
        '''
html_end = '''
        </body>
    </html>
    '''
img = f"<img src='{image_link}' alt='{last_game}'>"

html = html_start + "\n" + img + "\n" + html_end

print(html)
with open("C:\\Users\\Eder\\PycharmProjects\\skidrow-last-cracked-game-alert\\last_game.txt", "r") as file:
    if file.read() == last_game:
        print("SAME GAME")
    else:
        print("Writing new game and sending email")
        with open("C:\\Users\\Eder\\PycharmProjects\\skidrow-last-cracked-game-alert\\last_game.txt", "w") as file2:
            file2.write(last_game)

        email_message = MIMEMultipart()
        email_message['From'] = email_from
        email_message['To'] = email_to
        email_message['Subject'] = f'New Cracked Game: {last_game} - {date.today()}'
        email_message.attach(MIMEText(html, "html"))
        email_string = email_message.as_string()

        connection.sendmail(from_addr=email_from, to_addrs=email_to, msg=email_string)
