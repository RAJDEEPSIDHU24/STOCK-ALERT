from email.message import EmailMessage
import inspect
import textwrap
import smtplib
class SendEmail():
    def __init__(self, dict_of_companies_messages) -> None:
        self.dict_of_companies_messages = dict_of_companies_messages
        self.dict_is_not_empty = bool(self.dict_of_companies_messages)
        self._mail_message = ""
        self.create_mail_message()
    @property
    def mail_message(self):
        return self._mail_message
    def create_mail_message(self):
        for key, value in self.dict_of_companies_messages.items():
            self._mail_message += f"\n\n{value}\n"
        self._mail_message = inspect.cleandoc(self._mail_message)
        self._mail_message = textwrap.dedent(self._mail_message)
    def send_mails(self, to_addrs_mail, your_email, your_password):
        if self.dict_is_not_empty:
            msg = EmailMessage()
            msg.set_content(self._mail_message)
            msg["Subject"] = "📈 Stock Alert - Indian Companies"
            msg["To"] = to_addrs_mail
            server = smtplib.SMTP_SSL("smtp.gmail.com", port=465)
            server.login(user=your_email, password=your_password)
            server.send_message(msg)
            server.quit()
        else:
            raise ValueError("Dictionary of companies is empty.")
