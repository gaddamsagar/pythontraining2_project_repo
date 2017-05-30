"""This module contains code for work-from home"""
import logging
from tabulate import tabulate
import emailmodule
import dbops
DBCLASS = dbops.DbOperations()
EMAILCLASS = emailmodule.EmailClass()
logging.basicConfig(level=logging.DEBUG)


class Wfh(object):
    """This module performs workfromhome operations"""
    def applyworkfromhome(self, cur, dbcon, user, days, fromdate, todate):
        managerquery1 = "select manager from emp_details \
where empname = '{0}'".format(user)
#        print managerquery1
        manager = DBCLASS.browse(managerquery1, cur)
        leavetype, status = 'wfh', 'pending'
#        fromdate, todate = wfhdate, wfhdate
        emailquery = "select emailid from emp_details \
where empname = '{0}'".format(manager[0][0])
        manageremail = DBCLASS.browse(emailquery, cur)
        getidsquery = "select id from requests"
        idslist = DBCLASS.browse(getidsquery, cur)
        newid = idslist[len(idslist)-1][0]+1
        insertquery = "insert into requests values \
        ({0},'{1}','{2}','{3}',{4},'{5}','{6}','{7}')\
".format(newid, manager[0][0], user, leavetype, days, fromdate, todate, status)
        subject = "Subject: request id {0}: {1}\'s {2}\
request".format(newid, user, leavetype)
        if days == 1:
            wfhdate = "on {0}".format(fromdate)
        else:
            wfhdate = "from {0} to {1}".format(fromdate, todate)
        body = "Hi {3},\n\n{0} has applied for {1} {2}\nPlease\
login to approve/reject the request".format(user, leavetype, wfhdate, manager[0][0])
        msg = subject+"\n"+body
        if DBCLASS.insert(insertquery, cur, dbcon):
            EMAILCLASS.sendemail(msg, manageremail[0][0])

    def checkwfhstatus(self, user, cur):
        browsequery = "select * from requests where\
 empname = '{0}'".format(user)
        resp = DBCLASS.browse(browsequery, cur)
        if not resp:
            logging.info("No records found for '{0}' in\
requests".format(user))
            print "No records found in requests, try again"
            return True
        else:
            HEADER = [des[0] for des in cur.description]
            print tabulate(resp, HEADER)
            statuslist = [data[7] for data in resp]                    
            reqidlist = [data[0] for data in resp]
            leavetype = 'wfh'
            managerquery1 = "select manager from emp_details \
where empname = '{0}'".format(user)        
            manager = DBCLASS.browse(managerquery1, cur)
            emailquery = "select emailid from emp_details \
where empname = '{0}'".format(manager[0][0])
            manageremail = DBCLASS.browse(emailquery, cur)
            if 'pending' in statuslist:
                remindagain = raw_input("do you want to send a\
reminder email to manager for pending request? (y/n): ")
                if remindagain == 'y' or remindagain == 'yes':
                    while True:
                        reqid = input("enter the requestid : ")
                        if reqid in reqidlist:
                            while True:
                                if statuslist[reqidlist.index(reqid)] == '\
pending':
                                    subject = "Subject: \
Reminder request id {0}: {1}\'s {2} request".format(reqid, user, leavetype)
                                    body = "Hi {0}, \n\n{1} has sent you\
a reminder about request with id {2}.\nPlease login to approve/reject \
the request.".format(manager, user, reqid)
                                    msg = subject+"\n"+body
                                    EMAILCLASS.sendemail(msg, manageremail[0][0])
                                    return True
                                else:
                                    logging.error("Status of request\
with id {0} is not pending, You cannot send a reminder for this\
request").format(reqid)
                                    again = raw_input("do you want to\
try again (y/n):")
                                    if again == 'y' or again == 'yes':
                                        continue
                                    else:
                                        break
                        else:
                            logging.error("Entered request id\
is not valid, try again")
                            continue
                elif remindagain == 'n' or remindagain == 'no':
                    logging.info("not sending reminder email")

            else:
                logging.info("you don't have any prending\
requests to remind your manager")






if __name__ == "__main__":
    WFHCLASS = Wfh()
    host = "localhost"
    user = "root"
    pwd = "nexii"
    dbname = "leave_mgmt"
    dbcon = DBCLASS.getconnection(host, user, pwd, dbname)
    cur = dbcon.cursor()
    user = raw_input("enter user name: ")
    days = input("enter number of days: ")
    fromdate = raw_input("enter fromdate: ")
    todate = raw_input("enter to date: ")
    WFHCLASS.applyworkfromhome(cur, user, days, fromdate, todate)