"""This module is used to send emails """
import logging
import smtplib
ADMINEMAILID = "leavemanagementtool@gmail.com"
ADMINEMAILPWD = "leavemanagementtool@123"


class EmailClass(object):
    """This class is used to send emails"""
    def sendemail(self, msg, toemail):
        """This method takes imput as message and toemail id to send email"""
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(ADMINEMAILID, ADMINEMAILPWD)
            server.sendmail(ADMINEMAILID, toemail, msg)
            return True
        except Exception as err:
            logging.exception(err)

    def test1(self):
        """This is test method and will be used"""
        pass

    def test2(self):
        """This is test method and will be used"""
        pass


if __name__ == "__main__":
    EMAILCLASS = emailClass()
    TOEMAIL = "sagar.gaddam1@nexiilabs.com"
    MSG = """\
    Subject: python Test email from leave mgmt tool

    This is the Body of the test email2"""
    EMAILCLASS.sendemail(MSG, TOEMAIL)
