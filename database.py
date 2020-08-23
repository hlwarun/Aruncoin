import errors
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


# Perform Transction using your aruncoins
def perform_transcation(sender, recipient, balance):
    try:
        balance = float(balance)
    except ValueError:
        raise errors.TransactionError("The transction cannot be performed!")

    # Check if the user has sufficient balance
    if balance > get_balance(sender) and sender != "MINE":
        raise errors.InsufficientFund("You do not have sufficient balance!")
    # Check if user transfers funds to him/herself
    elif sender == recipient:
        raise errors.TransactionError("You cannot send balance to yourself!")
    # Check if user transfers negative funds
    elif balance <= 0.00:
        raise errors.TransactionError("You cannot send balance less than zero!")
    # Check if the username does not exists in the databse
    elif isnewuser(recipient):
        raise errors.TransactionError("The user with username you entered does not exists!")

    blockchain = get_blockchain()
    number = len(blockchain.chain) + 1
    data = "%s-->%s-->%s" %(sender, recipient, balance)
    blockchain.mining(Block(number, data=data))
    sync_blockchain(blockchain)



# Get informations of the balance of the user
def get_balance(username):
    balance = 0.00
    # Get the most recent blockchain
    blockchain = get_blockchain()
    for block in blockchain.chain:
        data = block.data.split('-->')
        # If user is sending money
        if username == data[0]:
            balance -= float(data[2])
        # If user is sending money
        if username == data[1]:
            balance += float(data[2])
    return balance

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

# Get the blockchain from the MySQL database
def get_blockchain():
    blockchain = Blockchain()
    blockchain_db = Table("blockchain", "number", "nonce", "hash_previous", "hash_current", "data")

    for block_db in blockchain_db.getall():
        blockchain.add_block(Block(int(block_db.get('number')), int(block_db.get('nonce')), block_db.get('hash_previous'), block_db.get('data')))
    return blockchain

# Sync blockchain with the new data
def sync_blockchain(blockchain):
    blockchain_db = Table("blockchain", "number", "nonce", "hash_previous", "hash_current", "data")
    blockchain_db.deleteall()

    for block in blockchain.chain:
        blockchain_db.insert(str(block.number), block.nonce, block.hash_previous, block.hash_current(), block.data)

# def delete_table_items():
#     users = Table("users", "first_name", "last_name", "username", "email", "password")
#     users.deleteall()


def sql_raw(execution):
    conn = db.connection.cursor()
    conn.execute(execution)
    db.connection.commit()
    conn.close()
