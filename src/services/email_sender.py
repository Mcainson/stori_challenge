import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from jinja2 import Template
from dotenv import load_dotenv

load_dotenv()
import mimetypes

class EmailSender:
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
    
    def send_summary(self, recipient, summary):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Stori - Transaction Summary'
        msg['From'] = self.smtp_user
        msg['To'] = recipient

        with open('src/templates/email_template.html', 'r') as f:
            template = Template(f.read())
        
        html_content = template.render(
            total_balance=f"${summary['total_balance']:.2f}",
            transactions_by_month=summary['transactions_by_month'],
            avg_credit=f"${summary['avg_credit']:.2f}",
            avg_debit=f"${summary['avg_debit']:.2f}"
        )
        
        msg.attach(MIMEText(html_content, 'html'))

        with open('src/templates/stori_logo.svg', 'rb') as f:
            img_data = f.read()
            mime_type, _ = mimetypes.guess_type('src/templates/stori_logo.svg')
            img = MIMEImage(img_data, _subtype=mime_type.split('/')[1] if mime_type else 'octet-stream')
            img.add_header('Content-ID', '<stori_logo>')
            msg.attach(img)

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
