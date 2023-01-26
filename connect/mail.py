# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os


class Set_Mail(object):

    def __init__(self):
        super().__init__()

    def settingMail(self):
        server = 'smtp.mail.ru'
        user = 'user@mail.ru'
        password = 'password'
        self.msg = MIMEMultipart("alternative")
        self.mail = smtplib.SMTP_SSL(server)
        self.mail.login(user, password)

    def sendMail(self, subject, recipients, text, filepath=None):
        sender = 'user@mail.ru'
        self.settingMail()

        html = '<html><head></head><body><p>'+text+'</p></body></html>'
        part_text = MIMEText(text, 'plain')
        part_html = MIMEText(html, 'html')
        if filepath is not None:
            basename = os.path.basename(filepath)
            part_file = MIMEApplication(open(filepath, 'rb').read())
            part_file.add_header(
                'Content-Disposition', 'attachment', filename=basename)
            self.msg.attach(part_file)
        self.msg['From'] = 'user@mail.ru'
        self.msg['To'] = ', '.join(recipients)
        self.msg['Subject'] = subject
        self.msg.attach(part_text)
        self.msg.attach(part_html)
        self.mail.sendmail(sender, recipients, self.msg.as_string())
        self.mail.quit()
