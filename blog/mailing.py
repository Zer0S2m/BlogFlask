import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import EMAIL
from config import EMAIL_PASSWORD


msg = MIMEMultipart()
message = "A new post came out!"

password = EMAIL_PASSWORD


def set_settings():
	msg['From'] = EMAIL
	msg['Subject'] = "Blog (Python/Flask)"


def send_messages(emails):
	set_settings()

	msg.attach(MIMEText(message, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com: 587')
	server.starttls()
	server.login(msg['From'], password)

	for email in emails:
		msg['To'] = email
		server.sendmail(msg['From'], msg['To'], msg.as_string())

	server.quit()
