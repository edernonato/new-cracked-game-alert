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
last_games = [game.text for game in soup.find_all(name="h2")]
last_game_links = [link.a.get('href') for link in soup.find_all(name="h2")]
image_tag = soup.select(selector="p a img")
image_tag = [image.get("data-lazy-src") for image in image_tag if image.get("data-lazy-src") is not None]

t = time.localtime()
html_start = f'''
    <html>
        <body>
        '''
html_end = '''
        </body>
    </html>
    '''
html_body = ""


with open("C:\\Users\\Eder\\PycharmProjects\\skidrow-last-cracked-game-alert\\last_game.txt", "r") as file:
    last_saved_game = file.read()
    if last_saved_game == last_games[0]:
        print("SAME GAME")
    else:
        if last_saved_game in last_games:
            max_index = last_games.index(last_saved_game)
        else:
            max_index = len(last_games)

        for game_index in range(max_index):
            image_link = image_tag[game_index]
            html_body += f"""
                        <h4>New Cracked Game: {last_games[game_index]} - {time.strftime("%H:%M:%S", t)} <br><br></h4>
                        <div>
                        <a href="{last_game_links[game_index]}" style="text-decoration:none; color: #11999E;">{last_games[game_index]}</a>
                        </div>
                        <img src='{image_link}' alt='{last_games[game_index]}'></img>
            """
        print("Writing new game and sending email")
        with open("C:\\Users\\Eder\\PycharmProjects\\skidrow-last-cracked-game-alert\\last_game.txt", "w") as file2:
            file2.write(last_games[0])

        if max_index == 0:
            last_game = last_games[0]
        else:
            last_game = f"{max_index} new Games"
        html = html_start + html_body + html_end
        email_message = MIMEMultipart()
        email_message['From'] = email_from
        email_message['To'] = email_to
        email_message['Subject'] = f'New Cracked Game: {last_game} - {date.today()}'
        email_message.attach(MIMEText(html, "html"))
        email_string = email_message.as_string()
        connection.sendmail(from_addr=email_from, to_addrs=email_to, msg=email_string)
        print(html)
