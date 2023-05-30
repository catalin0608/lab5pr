import smtplib
import poplib
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Autentificare utilizator pentru SMTP
def login_smtp(email, password):
    try:
        server = smtplib.SMTP('smtp.mail.ru', 587)
        server.starttls()
        server.login(email, password)
        return server
    except smtplib.SMTPAuthenticationError:
        print("Autentificare SMTP eșuată.")
        return None

# Autentificare utilizator pentru POP3
def login_pop3(email, password):
    try:
        server = poplib.POP3_SSL('pop.mail.ru', 995)
        server.user(email)
        server.pass_(password)
        return server
    except poplib.error_proto:
        print("Autentificare POP3 eșuată.")
        return None

# Autentificare utilizator pentru IMAP
def login_imap(email, password):
    try:
        server = imaplib.IMAP4_SSL('imap.mail.ru', 993)
        server.login(email, password)
        return server
    except imaplib.IMAP4.error:
        print("Autentificare IMAP eșuată.")
        return None

# Listare email-uri prin POP3
def list_emails_pop3(server):
    _, count, _ = server.list()
    for i in range(len(count)):
        msg_num = i + 1
        _, msg_lines, _ = server.retr(msg_num)
        msg = b'\r\n'.join(msg_lines).decode('utf-8')
        print(f"Email {msg_num}:\n{msg}\n")

# Listare email-uri prin IMAP
def list_emails_imap(server):
    server.select('INBOX')
    _, data = server.search(None, 'ALL')
    email_ids = data[0].split()
    for email_id in email_ids:
        _, msg_data = server.fetch(email_id, '(RFC822)')
        msg = msg_data[0][1].decode('utf-8')
        print(f"Email {email_id}:\n{msg}\n")

# Descărcare email cu atașament prin POP3
def download_email_pop3(server, msg_num):
    _, msg_lines, _ = server.retr(msg_num)
    msg = b'\r\n'.join(msg_lines).decode('utf-8')
    print(f"Email {msg_num}:\n{msg}\n")

# Descărcare email cu atașament prin IMAP
def download_email_imap(server, msg_num):
    server.select('INBOX')
    _, msg_data = server.fetch(msg_num, '(RFC822)')
    msg = msg_data[0][1].decode('utf-8')
    print(f"Email {msg_num}:\n{msg}\n")

# Trimitere email doar cu text
def send_email_text(server, sender_email, receiver_email, subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print("Email trimis cu succes.")

# Trimitere email cu atașament
def send_email_attachment(server, sender_email, receiver_email, subject, body, attachment_path):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    attachment = open(attachment_path, 'rb')
    payload = MIMEBase('application', 'octet-stream')
    payload.set_payload((attachment).read())
    encoders.encode_base64(payload)
    payload.add_header('Content-Disposition', 'attachment', filename=attachment_path.split('/')[-1])
    message.attach(payload)

    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print("Email trimis cu succes.")

# Exemplu de utilizare
email = 'lab5pr@mail.ru'
password = 'parola'
receiver_email = 'ccepraga4@gmail.com'
subject = 'Salut!'
body = 'Bună, Acesta este un email trimis prin Python.'
attachment_path = 'cale_catre_fisier/fisier.txt'

smtp_server = login_smtp(email, password)
if smtp_server:
    send_email_text(smtp_server, email, receiver_email, subject, body)
    smtp_server.quit()

pop3_server = login_pop3(email, password)
if pop3_server:
    list_emails_pop3(pop3_server)
    download_email_pop3(pop3_server, 1)
    pop3_server.quit()

imap_server = login_imap(email, password)
if imap_server:
    list_emails_imap(imap_server)
    download_email_imap(imap_server, b'1')
    imap_server.logout()
