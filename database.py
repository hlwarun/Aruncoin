from block import Block
from chain import Blockchain
from app import db, session

class Table():
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" %",".join(args)
        self.column_list = args

        if isnewtable(table_name):
            create_data = ""
            for column in self.column_list:
                create_data += "%s varchar(100)," %column

            conn = db.connection.cursor()
            print("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            conn.execute("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            conn.close()

    def insert(self, *args):
        data = ""
        for arg in args:
            data += "\"%s\"," %(arg)

        conn = db.connection.cursor()
        conn.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns, data[:len(data)-1]))
        db.connection.commit()
        conn.close()

    def getall(self):
        conn = db.connection.cursor()
        result = conn.execute("SELECT * FROM %s" %self.table)
        data = conn.fetchall(); return data

    def getone(self, search, value):
        data = {}; conn = db.connection.cursor()
        result = conn.execute("SELECT * FROM %s WHERE %s = \"%s\"" %(self.table, search, value))
        if result > 0: data = conn.fetchone()
        conn.close(); return data

    def drop(self):
        conn = db.connection.cursor()
        conn.execute("DROP TABLE %s" %self.table)
        conn.close()

    def deleteone(self, search, value):
        conn = db.connection.cursor()
        conn.execute("DELETE from %s where %s = \"%s\"" %(self.table, search, value))
        db.connection.commit(); conn.close()

    def deleteall(self):
        self.drop()
        self.__init__(self.table, *self.column_list)


# Check if the table exists already in the database
def isnewtable(name):
    conn = db.connection.cursor()
    try:
        result = conn.execute("SELECT * from %s" %name)
        conn.close()
    except:
        return True
    else:
        return False

# Check if the user does not exists already in the database
def isnewuser(username):
    users = Table("users", "first_name", "last_name", "username", "email", "password")
    data = users.getall()
    usernames = [user.get('username') for user in data]

    return False if username in usernames else True



def sql_raw(execution):
    conn = db.connection.cursor()
    conn.execute(execution)
    db.connection.commit()
    conn.close()
