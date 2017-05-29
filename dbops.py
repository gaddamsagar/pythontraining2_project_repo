"""This module performs db operations"""
import logging
import MySQLdb
from tabulate import tabulate
logging.basicConfig(level=logging.DEBUG)


class DbOperations(object):
    """
    This class is used for db operations
    """

    def getconnection(self, host, user, pwd, dbname):
        """This module connects to the db and returns the cursor for\
        dboperatios"""
        dbcon = MySQLdb.connect(host, user, pwd, dbname)
        #cursor = dbcon.cursor()
        return dbcon#cursor

    def create_table(self, query, cur):
        """This module takes a query and cursor as argumnets and \
        creates table in the database"""
        try:
            cur.execute(query)
            logging.info("created a table")
            return True
        except Exception as err:
            logging.exception(err)
            return False

    def insert(self, query, cur,dbcon):
        """This module takes query and cursor and inserts data into table"""
        try:
            cur.execute(query)
            logging.info("inserting data into table")
            dbcon.commit()
            return True
        except Exception as err:
            logging.exception(err)
            return False

    def browse(self, query, cur):
        """This module takes query and cursor and browses data from db"""
        try:
            cur.execute(query)
            data = cur.fetchall()
            logging.info("reading data from table")
#            print data
            return data
        except Exception as err:
            logging.exception(err)
            return False


if __name__ == "__main__":
    DBCLASS = DbOperations()
    HOST = "localhost"
    USER = "root"
    PWD = "nexii"
    DBNAME = "leave_mgmt"
    dbcon = DBCLASS.getconnection(HOST, USER, PWD, DBNAME)
    CUR = dbcon.cursor()
    TBNAME = "emp_details"
    BROWSEQUERY = "select * from {0}".format(TBNAME)
    DATA = DBCLASS.browse(BROWSEQUERY, CUR)
    logging.info("Reading header from table '{0}'".format(TBNAME))    
    HEADER = [description[0] for description in CUR.description]
    print tabulate(DATA, HEADER)+"\n"
    TBNAME = "credentials"
    BROWSEQUERY = "select * from {0}".format(TBNAME)
    DATA = DBCLASS.browse(BROWSEQUERY, CUR)
    logging.info("Reading header from table '{0}'".format(TBNAME))
    HEADER = [description[0] for description in CUR.description]
    print tabulate(DATA, HEADER)

    dbcon.close()
