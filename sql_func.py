## the sql functions
import sqlite3
from flask import g,Flask

path='/Volumes/Macintosh HD/Users/vishnu/Desktop/tcs_bank/app'
DATABASE = '/Volumes/Macintosh HD/Users/vishnu/Desktop/tcs_bank/app/bank.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    # db = getattr(g, '_database', None)
    # if db is None:
    #     db = g._database = sqlite3.connect(DATABASE)
    # return db
    return sqlite3.connect(DATABASE)

def init_db_customer(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE customers(
		ws_ssn INTEGER NOT NULL PRIMARY KEY,
		ws_cust_id INTEGER NOT NULL PRIMARY KEY,
		ws_name TEXT,
		ws_adrs TEXT,
		ws_age INTEGER
		)""")

def init_db_account(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE account(
		ws_cust_id INTEGER NOT NULL PRIMARY KEY,
		ws_acct_id INTEGER NOT NULL PRIMARY KEY,
		ws_acct_type TEXT,
		ws_acct_balance INTEGER,
		ws_acct_crdate TEXT,
		ws_acct_lasttrdate TEXT,
		ws_acct_duration INTEGER
		)""")

def init_db_transactions(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE transactions(
		ws_cust_id INTEGER NOT NULL PRIMARY KEY,
		ws_acct_id INTEGER NOT NULL PRIMARY KEY,
		ws_amt INTEGER,
		ws_trxn_date TEXT,
		ws_src_typ TEXT,
		ws_tgt_typ TEXT
		)""")

def init_db_user_store(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE user_store(
		login_id text NOT NULL PRIMARY KEY,
		pass text,
		create_time timestamp,
		type Text 
		)""")

def get_user(db,**det):
	db.row_factory = dict_factory
	cur=db.cursor()
	cur.execute("SELECT * FROM user_store where login_id = (?)",(det["username"],))
	return cur.fetchone()



def del_table(db,name):
	cur=db.cursor()
	db.execute("DROP TABLE "+name)

def add_new_cus(db,**det):
	cur = db.cursor()
	cur.execute("INSERT INTO customers (ws_ssn,ws_cust_id,ws_name,ws_adrs,ws_age) VALUES (?,?,?,?,?)",
    	(det["ss"],det["cid"],det["name"],det["addr"],det["age"]))
	return True

def get_cus_det(db):
	cur=db.cursor()
	cur.execute("SELECT * FROM customers")
	return cur.fetchall()

         

if __name__=='__main__':
	# init_db()
	pass

