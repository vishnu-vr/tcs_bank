## the sql functions
import sqlite3
from flask import g,Flask
from datetime import date

path='/Volumes/Macintosh HD/Users/vishnu/Desktop/tcs_bank/app'
# DATABASE = '/Volumes/Macintosh HD/Users/vishnu/Desktop/tcs_bank/app/bank.db'
DATABASE="bank.db"

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

def init_db_customers(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE customers(
		ws_ssn INTEGER NOT NULL UNIQUE,
		ws_cust_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		ws_name TEXT,
		ws_adrs TEXT,
		ws_age INTEGER
		)""")

def init_db_account(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE account(
		ws_cust_id INTEGER NOT NULL,
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
		ws_acct_id INTEGER NOT NULL,
		ws_amt INTEGER,
		ws_trxn_date TEXT,
		ws_src_typ TEXT,
		ws_tgt_typ TEXT
		)""")
# Customer ID, Account ID, Account Type, Status, Message, Last Updated
def init_account_status(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE account_status(
		ws_cust_id INTEGER NOT NULL PRIMARY KEY,
		ws_acct_id INTEGER NOT NULL,
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
		created_time text,
		type Text 
		)""")

def get_user(**det):
	db.row_factory = dict_factory
	cur=db.cursor()
	cur.execute("SELECT * FROM user_store where login_id = (?)",(det["login_id"],))
	return cur.fetchone()

def add_new_user(**det):
	cur = db.cursor()
	cur.execute("INSERT INTO user_store VALUES (?,?,?,?)",(det["login_id"],det["pass"],str(date.today()),det["type"]))
	db.commit()
	return True

def del_table(name):
	cur=db.cursor()
	db.execute("DROP TABLE "+name)

def add_new_cus(**det):
	db=get_db()
	cur = db.cursor()
	try:
		cur.execute("INSERT INTO customers (ws_ssn,ws_name,ws_adrs,ws_age) VALUES (?,?,?,?)",
	    	(int(det["ws_ssn"]),det["ws_name"],det["ws_adrs"]+"#"+det["state"]+"#"+det["city"],int(det["ws_age"])))
		db.commit()
	except Exception as e :
		db.rollback()
		return False
	finally:
		db.close()
	return True

def get_cus_det(db):
	cur=db.cursor()
	cur.execute("SELECT * FROM customers")
	return cur.fetchall()

         

if __name__=='__main__':
	# init_db()
	# init_db_user_store()
	db=get_db()
	usr={
	"login_id":"cash12",
	"pass":"cash12",
	"created_time":"1234-02-12",
	"type":"C"
	}
	c={'ws_ssn': "123123123", 'ws_name': 'vishnu', 'ws_age': "30", 'ws_adrs': 'palaace road', 'state': 'Berlin', 'city': 'Berlin'}
	# add_new_user(get_db(),**d)
	# add_new_cus(get_db(),)
	# init_db_customers()
	add_new_cus(db,**c)


