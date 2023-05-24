import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
def send_me():
    sender = "report.age.gender@gmail.com"
    reciver = "ufukkirmizigedik1984@gmail.com"
    body_of_email = "Telegram report"
    msg = MIMEMultipart()
    msg["Subject"] = "Отчет от Бота"
    msg["From"] = "report.age.gender@gmail.com"
    msg["To"] = "ufukkirmizigedik1984@gmail.com"
    part = MIMEBase("application", "octet-stream")
    part.set_payload(open("/Users/ufukkirmizigedik/Desktop/reportbot/ops.db", "rb").read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename = ops.db")
    msg.attach(part)
    s = smtplib.SMTP_SSL(host= "smtp.gmail.com" , port=465)
    s.login(user=sender, password="mtuiznanajsjchun")
    s.sendmail(sender,reciver,msg.as_string())
    s.quit()
    print('email sent')