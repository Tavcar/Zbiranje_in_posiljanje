# -*- coding: utf-8 -*-
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
import smtplib
from secret import moje_geslo
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

url = "https://scrapebook22.appspot.com"
response = urlopen(url).read()
soup = BeautifulSoup(response)

csv_file = open("email.csv", "w")

for link in soup.findAll("a"):
    if link.string == "See full profile":
        person_url = url + link["href"]
        person_html = urlopen(person_url).read()
        person_soup = BeautifulSoup(person_html)
        email = person_soup.find("span", attrs={"class": "email"}).string
        name = person_soup.findAll("h1")[1].string
        city = person_soup.find("span", attrs={"data-city": True}).string
        csv_file.write(name + ", " + email + ", " + city + "\n")

csv_file.close()

posiljatelj = "from@gmail.com"
prejemnik = "to@gmail.com"
geslo = moje_geslo

zadeva = "Lep pozdrav iz Python programa"
vsebina = "Pošiljam datoteko z zbranimi e-maili."

msg = MIMEMultipart()
msg["From"] = posiljatelj
msg["To"] = prejemnik
msg["Subject"] = zadeva

msg.attach(MIMEText(vsebina))

filename = "email.csv"
f = file(filename)
attachment = MIMEText(f.read())
attachment.add_header('Content-Disposition', 'attachment', filename=filename)
msg.attach(attachment)

try:
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()

    server.login(user=posiljatelj, password=geslo)
    server.sendmail(from_addr=posiljatelj, to_addrs=prejemnik, msg=msg.as_string())
    server.quit()
    print "Sporočilo je bilo uspešno poslano!"
except Exception as e:
    print "NAPAKA!"
    print e