"""This module validates user credentials to access leave mgmt tool """

import getpass
import logging
import calendar
from datetime import datetime
import dbops
import emailmodule
logging.basicConfig(level=logging.DEBUG)
DBCLASS = dbops.DbOperations()
EMAILCLASS = emailmodule.EmailClass()

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
                for pwdcount in range(3):
                    index1 = self.userlist.index(user)
                    pwd = getpass.getpass('Password:')
                    pwdcount += 1
                    if pwd == self.pwdlist[index1]:
                        logging.info("user logged in successfully")
                        return True,user,self.dbcon
                        break
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
        print calendar.month(year,month)
        while True:            
            print "select 1 to display full calendar for current year"
            print "select 2 to display calendar for other months in current year"
            print "select 3 to display calendar for your selected month and year"
            print "select 'X' to go back to main menu"
            option = raw_input("option : ")
            if option == "1":
                year = now.year
                c1 = calendar.TextCalendar()
                print c1.formatyear(2017)
            elif option == "2":
                while True:
                    try:
                        year = now.year
                        month = input("enter the number of month : ")
                        print calendar.month(year,month)
                        break
                    except Exception as err:
                        logging.exception(err)
                        print "try again"
            elif option == "3":
                while True:
                    try:
                        year = input("enter the year : ")
                        month = input("enter the number of month : ")
                        print calendar.month(year,month)
                        break
                    except Exception as err:
                        logging.exception(err)
                        print "try again"
            elif option == "x" or option == 'X':
                break

    def workfromhome(self,user,dbcon):
        """This module takes input as user and performs his WFH operations """
        while True:
            print "select 1 to apply for work from home or \n\
select 2 to check status of wfh\nselect 3 to go back to main menu"
            option = raw_input("option : ")
            if option == "1":
                while True:
                  try:
                    days = input("how many days \n enter 0 (zero) to go back\
to previous menu : ")
                    if days == 0:
                        break
                    elif days == 1:
                        wfhdate = raw_input("enter date (yyyy-mm-dd): ")
                        fromdate,todate = wfhdate,wfhdate
                        #print wfhdate
                        managerquery = "select manager from emp_details where\
 empname = '{0}'".format(user)
                        manager = DBCLASS.browse(managerquery,self.cur)
                        #print manager[0][0]
                        LEAVETYPE,STATUS = 'wfh','pending'
                        fromdate,todate = wfhdate,wfhdate
                        emailquery = "select emailid from emp_details where\
 empname = '{0}'".format(manager[0][0])
                        manageremail = DBCLASS.browse(emailquery,self.cur)
                        getidsquery = "select id from requests"
                        idslist = DBCLASS.browse(getidsquery,self.cur)
                        newid = idslist[len(idslist)-1][0]+1
                        insertquery = "insert into requests values ({0},'{1}'\
,'{2}','{3}',{4},'{5}','{6}','{7}')".\
format(newid, manager[0][0], user, LEAVETYPE, days, fromdate, todate, STATUS)
                        try:
                            DBCLASS.insert(insertquery,self.cur,dbcon)
                        except Exception as err:
                            logging.exception(err)
                        useremailquery = "select emailid from emp_details where\
 empname = '{0}'".format(user)
                        useremail = DBCLASS.browse(useremailquery,self.cur)
                        subject = "Subject: request id {0}: {1}\'s {2} request".\
format(newid, user, LEAVETYPE)
                        body = "{0} has applied for {1} on {2}\n Please login to\
 approve/reject the request".format(user,\
 LEAVETYPE, wfhdate)
                        msg = subject+"\n"+body
                        try:
                            EMAILCLASS.sendemail(msg,manageremail)
                        except Exception as err:
                            logging.exception(err)
                        break
                    elif days > 1 or days < 5:
                        fromdate = raw_input("enter from date (yyyy-mm-dd): ")
                        todate = raw_input("enter to date (yyyy-mm-dd): ")
                        managerquery = "select manager from emp_details where\
 empname = '{0}'".format(user)
                        manager = DBCLASS.browse(managerquery,self.cur)
                        #print manager[0][0]
                        LEAVETYPE,STATUS = 'wfh','pending'
                        emailquery = "select emailid from emp_details where\
 empname = '{0}'".format(manager[0][0])
                        manageremail = DBCLASS.browse(emailquery,self.cur)
                        getidsquery = "select id from requests"
                        idslist = DBCLASS.browse(getidsquery,self.cur)
                        newid = idslist[len(idslist)-1][0]+1
                        insertquery = "insert into requests values ({0},'{1}'\
,'{2}','{3}',{4},'{5}','{6}','{7}')".\
format(newid, manager[0][0], user, LEAVETYPE, days, fromdate, todate, STATUS)
                        try:
                            DBCLASS.insert(insertquery,self.cur,dbcon)
                        except Exception as err:
                            logging.exception(err)
                        useremail = DBCLASS.browse(useremailquery,self.cur)
                        subject = "Subject: request id {0}: {1}\'s {2} request".\
format(newid, user, LEAVETYPE)
                        body = "{0} has applied for {1} from {2} to {3}\n\nPlease login to\
 approve/reject the request".format(user,\
 LEAVETYPE, fromdate, todate)
                        msg = subject+"\n"+body
                        try:
                            EMAILCLASS.sendemail(msg,manageremail)
                        except Exception as err:
                            logging.exception(err)
                        break


                  except Exception as err:
                        logging.exception(err)
                        continue
            elif option == '2':
                pass
                return True

            elif option == '3':
                return True


if __name__ == "__main__":
    USERLOGINCL = UserLogin()
    validated = False
    validated,user,dbcon = USERLOGINCL.validate()
    while validated:
        print "enter 1 for WFH or\nenter 2 for Leaves or\nenter 3 to \
Display calendar or \nenter 'X' to logout"
        option = raw_input("option : ")
        if option == "1":
            USERLOGINCL.workfromhome(user,dbcon)
            logging.info("WFH code under progress")
            pass
        elif option == "2":
            logging.info("code under progress")
            pass
        elif option == "3":
            #year = input("enter the year : ")
            #month = input("enter the number of month : ")
            USERLOGINCL.displaycalendar()
        elif option == 'X' or option =='x':
            dbcon.close()
            logging.info("succesfully logged out")
            break