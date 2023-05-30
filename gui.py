import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import tkinter as tk
from tkinter import filedialog

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

# Funcție pentru atașarea unui fișier
def attach_file():
    attachment_path = filedialog.askopenfilename()
    attachment_entry.delete(0, tk.END)
    attachment_entry.insert(tk.END, attachment_path)

# Funcție pentru trimiterea email-ului cu atașament
def send_email_attachment(server, sender_email, receiver_email, subject, body, attachment_path):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    if attachment_path:
        attachment = open(attachment_path, "rb")

        part = MIMEBase("application", "octet-stream")
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=attachment_path)
        message.attach(part)

    server.send_message(message)

# Funcție pentru trimiterea email-ului
def send_email():
    sender_email = sender_entry.get()
    password = password_entry.get()
    receiver_email = receiver_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", tk.END)

    smtp_server = login_smtp(sender_email, password)
    if smtp_server:
        send_email_attachment(smtp_server, sender_email, receiver_email, subject, body, attachment_entry.get())
        smtp_server.quit()

        # Resetează valorile câmpurilor
        sender_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        receiver_entry.delete(0, tk.END)
        subject_entry.delete(0, tk.END)
        body_text.delete("1.0", tk.END)
        attachment_entry.delete(0, tk.END)

# Crearea ferestrei principale
window = tk.Tk()
window.title("Aplicație de trimitere email")
window.geometry("500x550")
window.configure(bg="#1c1e26")

# Frame-ul principal
main_frame = tk.Frame(window, bg="#1c1e26")
main_frame.pack(padx=20, pady=10)

# Etichete și câmpuri de introducere
sender_label = tk.Label(main_frame, text="De la:", font=("Helvetica", 14, "bold"), bg="#1c1e26", fg="#ffffff")
sender_label.grid(row=0, column=0, sticky="w")
sender_entry = tk.Entry(main_frame, font=("Helvetica", 12), relief=tk.SOLID, bd=1)
sender_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

password_label = tk.Label(main_frame, text="Parolă:", font=("Helvetica", 14, "bold"), bg="#1c1e26", fg="#ffffff")
password_label.grid(row=1, column=0, sticky="w")
password_entry = tk.Entry(main_frame, show="*", font=("Helvetica", 12), relief=tk.SOLID, bd=1)
password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

receiver_label = tk.Label(main_frame, text="Către:", font=("Helvetica", 14, "bold"), bg="#1c1e26", fg="#ffffff")
receiver_label.grid(row=2, column=0, sticky="w")
receiver_entry = tk.Entry(main_frame, font=("Helvetica", 12), relief=tk.SOLID, bd=1)
receiver_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

subject_label = tk.Label(main_frame, text="Subiect:", font=("Helvetica", 14, "bold"), bg="#1c1e26", fg="#ffffff")
subject_label.grid(row=3, column=0, sticky="w")
subject_entry = tk.Entry(main_frame, font=("Helvetica", 12), relief=tk.SOLID, bd=1)
subject_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

body_label = tk.Label(main_frame, text="Mesaj:", font=("Helvetica", 14, "bold"), bg="#1c1e26", fg="#ffffff")
body_label.grid(row=4, column=0, sticky="w")
body_text = tk.Text(main_frame, height=8, width=30, font=("Helvetica", 12), relief=tk.SOLID, bd=1)
body_text.grid(row=4, column=1, padx=10, pady=5, sticky="we")

attachment_label = tk.Label(main_frame, text="Atașament:", font=("Helvetica", 14, "bold"), bg="#1c1e26", fg="#ffffff")
attachment_label.grid(row=5, column=0, sticky="w")
attachment_entry = tk.Entry(main_frame, font=("Helvetica", 12), relief=tk.SOLID, bd=1)
attachment_entry.grid(row=5, column=1, padx=10, pady=5, sticky="we")

attach_button = tk.Button(main_frame, text="Atașează fișier", command=attach_file, font=("Helvetica", 12), bg="#0078d4", fg="#ffffff", relief=tk.FLAT)
attach_button.grid(row=6, column=0, columnspan=2, pady=10)

send_button = tk.Button(main_frame, text="Trimite", command=send_email, font=("Helvetica", 16, "bold"), bg="#0078d4", fg="#ffffff", relief=tk.FLAT)
send_button.grid(row=7, column=0, columnspan=2, pady=10)

window.mainloop()
