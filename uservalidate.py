"""This module validates user credentials to access leave mgmt tool """

import getpass
import logging
import calendar
import dbops
logging.basicConfig(level=logging.DEBUG)
DBCLASS = dbops.DbOperations()


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
        cur = DBCLASS.getconnection(host, user, pwd, dbname)
        tbname = "credentials"
        browsequery = "select * from {0}".format(tbname)
        data = DBCLASS.browse(browsequery, cur)
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
                        return True
                        break
                else:
                    logging.error("3 password attemps failed")
                    break
                break

    def test(self):
        """more code to add"""
        pass


if __name__ == "__main__":
    USERLOGINCL = UserLogin()
    validated = USERLOGINCL.validate()
    while validated:
        print "enter 1 for WFH or\nenter 2 for Leaves or\nenter 3 to Display calendar or \nenter 'X' to logout"
        option = raw_input("option : ")
        if option == "1":
            logging.info("code under progress")
            pass
        elif option == "2":
            logging.info("code under progress")
            pass
        elif option == "3":
            year = input("enter the year : ")
            month = input("enter the number of month : ")
            print calendar.month(year,month)
        elif option == 'X' or option =='x':
            logging.info("succesfully logged out")
            break
