"""This module validates user credentials to access leave mgmt tool """

import getpass
import logging
import calendar
from datetime import datetime
from tabulate import tabulate
import dbops
import emailmodule
import wfh
logging.basicConfig(level=logging.DEBUG)
DBCLASS = dbops.DbOperations()
EMAILCLASS = emailmodule.EmailClass()
WFHCLASS = wfh.Wfh()


class UserLogin(object):
    """
    This class contains code for checking if a user exists in db when he tries
    to login to access Leave management tools and validates his/her credentials
    """
    def __init__(self):
        """in init method code connects to db and reads data"""
        host = "localhost"
        user = "root"
        pwd = "nexii"
        dbname = "leave_mgmt"
        self.dbcon = DBCLASS.getconnection(host, user, pwd, dbname)
        self.cur = self.dbcon.cursor()
        tbname = "credentials"
        browsequery = "select * from {0}".format(tbname)
        data = DBCLASS.browse(browsequery, self.cur)
        self.userlist = [i[0] for i in data]
        self.pwdlist = [i[1] for i in data]
        self.mgrlist = [i[2] for i in data]
        print self.userlist

    def validate(self):
        """This module validates the user credentials"""
        pwdcount = 0
        while True:
            user = raw_input("enter user name :")
            if user not in self.userlist:
                logging.error("user does not exist try again")
                continue
            else:
                index1 = self.userlist.index(user)
                for pwdcount in range(3):
                    pwd = getpass.getpass('Password:')
                    pwdcount += 1
                    if pwd == self.pwdlist[index1]:
                        logging.info("user logged in successfully")
                        if self.mgrlist[index1] == "yes":
                            logging.info("manager logged in")
                            pass
                            return False, user, self.dbcon
                        else:
                            return True, user, self.dbcon
                else:
                    logging.error("3 password attemps failed")
                    break
                break

    def displaycalendar(self):
        """This module is used for diplaying calendar"""
        now = datetime.now()
        year = now.year
        month = now.month
        calendar.setfirstweekday(6)
        print calendar.month(year, month)
        while True:
            print "select 1 to display full calendar for current year"
            print "select 2 to display calendar for other months in \
current year"
            print "select 3 to display calendar for your selected \
month and year"
            print "select 'X' to go back to main menu"
            option = raw_input("option : ")
            if option == "1":
                year = now.year
                CALCLASS = calendar.TextCalendar()
                print CALCLASS.formatyear(2017)
            elif option == "2":
                while True:
                    try:
                        year = now.year
                        month = input("enter the number of month : ")
                        print calendar.month(year, month)
                        break
                    except Exception as err:
                        logging.exception(err)
                        print "try again"
            elif option == "3":
                while True:
                    try:
                        year = input("enter the year : ")
                        month = input("enter the number of month : ")
                        print calendar.month(year, month)
                        break
                    except Exception as err:
                        logging.exception(err)
                        print "try again"
            elif option == "x" or option == 'X':
                break

    def workfromhome(self, user, dbcon):
        """This module takes input as user and performs his WFH operations """
        while True:
            print "select 1 to apply for work from home or \n\
select 2 to check status of wfh\nselect 3 to go back to main menu"
            option = raw_input("option : ")
            if option == "1":
                while True:
                    try:
                        days = input("how many days \n enter 0 (zero)\
 to go back to previous menu : ")
                        if days == 0:
                            break
                        elif days == 1:
                            wfhdate = raw_input("enter date (yyyy-mm-dd): ")
                            fromdate, todate = wfhdate, wfhdate
                            WFHCLASS.applyworkfromhome(self.cur, dbcon, user, days, fromdate, todate)
                            break
                        elif days > 1 and days < 6:
                            fromdate = raw_input("enter from date (yyyy-mm\
-dd): ")
                            todate = raw_input("enter to date (yyyy-mm-dd)\
: ")
                            WFHCLASS.applyworkfromhome(self.cur, dbcon, user, days, fromdate, todate)
                            break
                        else:
                            logging.error("Maximum allowed is 5, try again")
                            continue
                    except Exception as err:
                        logging.exception(err)
                        continue
            elif option == '2':
                WFHCLASS.checkwfhstatus(user, self.cur)

            elif option == '3':
                return True


if __name__ == "__main__":
    USERLOGINCL = UserLogin()
    VALIDATED = False
    VALIDATED, user, DBCON = USERLOGINCL.validate()
    while VALIDATED:
        print "enter 1 for WFH or\nenter 2 for Leaves or\nenter 3 to \
Display calendar or \nenter 'X' to logout"
        option = raw_input("option : ")
        if option == "1":
            USERLOGINCL.workfromhome(user, DBCON)
            logging.info("WFH code under progress")
            pass
        elif option == "2":
            logging.info("code under progress")
            pass
        elif option == "3":
            USERLOGINCL.displaycalendar()
        elif option == 'X' or option == 'x':
            DBCON.close()
            logging.info("succesfully logged out")
            break
