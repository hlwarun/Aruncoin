from app import db, session

class Table():
    def __init__(self, table_name, *args):
        self.table = table_name
        # we will use each arguments in args as columns of the table
        self.columns = '(%s)'%','.join(args)

        if isnewtable(table_name):
            create_data = ""
            for column in self.columnsList:
                create_data += "%s varchar(100)," %column

            cur = mysql.connection.cursor()
            print("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            cur.execute("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            cur.close()

     def getall(self):
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s" %self.table)
        data = cur.fetchall(); return data

    def getone(self, search, value):
        data = {}; cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s WHERE %s = \"%s\"" %(self.table, search, value))
        if result > 0: data = cur.fetchone()
        cur.close(); return data

    def deleteone(self, search, value):
        cur = mysql.connection.cursor()
        cur.execute("DELETE from %s where %s = \"%s\"" %(self.table, search, value))
        mysql.connection.commit(); cur.close()

    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" %self.table)
        cur.close()

    def insert(self, *args):
        data = ""
        for arg in args:
            data += "\"%s\"," %(arg)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns, data[:len(data)-1]))
        mysql.connection.commit()
        cur.close()



def isnewtable(name):
    cur = db.connection.cursor()

    try:
        cur.execute("SELECT * from %s"%sname)
        cur.close
    except:
        return True
    else:
        return False

def sql_raw(execution):
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()


def isnewuser(username):
    users = Table("users", "name", "email", "username", "password")
    data = users.getall()
    usernames = [user.get('username') for user in data]

    return False if username in usernames else True
