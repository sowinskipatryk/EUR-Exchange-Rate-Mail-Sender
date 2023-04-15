import smtplib
import requests
from creds import API_KEY, ADDR_FROM, ADDR_TO, PASSWD
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

AMOUNT = 3600

url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/EUR'

r = requests.get(url, headers=None)
data = r.json()
rate_today = data['conversion_rates']['PLN']
total = AMOUNT * rate_today

with open('history.txt', 'r') as file:
    for line in file:
        last_line = line
    rate_yesterday = float(last_line.replace('\n', '').split(',')[1])
    rate_diff = ((rate_today / rate_yesterday) - 1) * 100

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(ADDR_FROM, PASSWD)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'{AMOUNT} EUR @ {rate_today} = {total:.2f} PLN'
    msg['From'] = ADDR_FROM
    msg['To'] = ADDR_TO

    text = f"Yesterday's exchange rate: {rate_yesterday} [{'+' if rate_diff >= 0 else ''}{rate_diff:.1f}%]"

    html = f"""\
    <html>
      <body>
        <p>Yesterday's exchange rate: {rate_yesterday} [{'+' if rate_diff >= 0 else ''}{rate_diff:.1f}%]</p>
      </body>
    </html>
    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    smtp.sendmail(ADDR_FROM, ADDR_TO, msg.as_string())

time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
new_line = f"{time}, {rate_today}, {total:.2f}\n"

with open('history.txt', 'a') as file:
    file.write(new_line)
