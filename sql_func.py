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
def split_addr(det):
	addr=det["ws_adrs"]
	adr,state,city=addr.split("#")
	det["ws_adrs"]=adr
	det["state"]=state
	det["city"]=city
	return det

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
	db=get_db()
	db.row_factory = dict_factory
	cur=db.cursor()
	cur.execute("SELECT * FROM user_store where login_id = (?)",(det["login_id"],))
	user=cur.fetchone()
	db.close()
	return user

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
	return False

def update_cus(**det):
	db=get_db()
	db.row_factory = dict_factory
	cur = db.cursor()
	updatable=["ws_name","ws_age","ws_adrs"]
	colunm_names=list(det.keys())
	print(colunm_names)
	try:
		for cn in colunm_names:
			if cn not in updatable:
				continue
			if cn=="ws_adrs":
				old_det=get_cus_det(**{"ws_cust_id":det["ws_cust_id"]})
				det["ws_adrs"]=det["ws_adrs"]+"#"+old_det["state"]+"#"+old_det["city"]
			cur.execute("UPDATE customers SET "+cn+" = ? where ws_cust_id = ?",(det[cn],det["ws_cust_id"]))
			print(cn)
		db.commit()
		return True
	except Exception as e :
		db.rollback()
		print(e)
		return False
	finally:
		db.close()
	return False

def get_cus_det(**det):
	db=get_db()
	db.row_factory = dict_factory
	cur = db.cursor()
	colunm_name=list(det.keys())[0]
	try:
		cur.execute("SELECT * FROM customers where "+colunm_name+" = (?)",(det[colunm_name],))
		customer_det=cur.fetchone()
		customer_det=split_addr(customer_det)
		# print(customer_det)
		db.commit()
		return customer_det
	except Exception as e :
		db.rollback()
		print(e)
		return False
	finally:
		db.close()
	return False

def del_cus(**det):
	db=get_db()
	db.row_factory = dict_factory
	cur = db.cursor()
	try:
		customer_det=get_cus_det(**det)
		cur.execute("DELETE FROM customers where ws_cust_id = (?)",(det["ws_cust_id"],))
		db.commit()
		return customer_det
	except Exception as e :
		db.rollback()
		print(e)
		return False
	finally:
		db.close()
	return False

         

if __name__=='__main__':
	# init_db()
	# init_db_user_store()
	usr={
	"login_id":"cash12",
	"pass":"cash12",
	"created_time":"1234-02-12",
	"type":"C"
	}
	c={"ws_name":"isham1" ,"ws_adrs":"puthur","state":"kerala","city":"thrissur","ws_ssn":"786643554","ws_age":"23"}
	c2={"ws_cust_id":2,"ws_name":"isham1" ,"ws_adrs":"ayyanthole1"}
	# add_new_user(get_db(),**d)
	add_new_cus(**c)
	# init_db_customers()
	# update_cus(**c2)
	# print(get_cus_det(**{"ws_cust_id":2}))


