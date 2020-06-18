## the sql functions
import sqlite3
from flask import g,Flask
from datetime import date,datetime

# path='/Volumes/Macintosh HD/Users/vishnu/Desktop/tcs_bank/app'
# DATABASE = '/Volumes/Macintosh HD/Users/vishnu/Desktop/tcs_bank/app/bank.db'
DATABASE="bank.db"

def update_cus_status(det,db):
	cur = db.cursor()
	updatable=["status","message","last_updated"]
	colunm_names=list(det.keys())
	try:
		for cn in colunm_names:
			if cn not in updatable:
				continue
			cur.execute("UPDATE cus_status SET "+cn+" = ? where ws_cust_id = ?",(det[cn],det["ws_cust_id"]))
		return True
	except Exception as e :
		db.rollback()
		print(e)
	return False

def add_cus_status(det,db):
	# db=get_db()
	cur=db.cursor()	
	try:
		cur.execute("INSERT INTO cus_status (ws_cust_id,ws_ssn,status,message,last_updated) VALUES (?,?,?,?,?)",
			(int(det["ws_cust_id"]),
				int(det["ws_ssn"]),
				det["status"],
				det["message"],
				str(datetime.now())
				))
		return True
	except Exception as e :
		print(e)
		db.rollback()
	return False

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
	# temp={"ws_name":"temp" ,"ws_adrs":"temp","state":"temp","city":"temp","ws_ssn":"000000000","ws_age":"00","ws_cust_id":"100000000"}
	cur.execute("insert into sqlite_sequence (name, seq) values (?, ?);",( "customers", 100000000 ));
	db.commit()
	db.close()

def init_db_account(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE account(
		ws_cust_id INTEGER NOT NULL,
		ws_acct_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		ws_acct_type TEXT,
		ws_acct_balance REAL,
		ws_acct_crdate TEXT,
		ws_acct_lasttrdate TEXT
		-- ws_acct_duration INTEGER
		)""")
	# temp={"ws_acct_type":"temp" ,"ws_acct_balance":00,"ws_acct_crdate":"temp","ws_acct_lasttrdate":"temp",
	# "ws_acct_id":"500000000","ws_cust_id":"temp"}
	cur.execute("insert into sqlite_sequence (name, seq) values (?, ?);",( "account", 500000000 ));
	db.commit()
	db.close()

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
	db.commit()
	db.close()

# Customer ID, Account ID, Account Type, Status, Message, Last_Updated
def init_account_status(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE account_status(
		ws_cust_id INTEGER NOT NULL PRIMARY KEY,
		ws_acct_id INTEGER NOT NULL ,
		ws_acct_type text,
		status TEXT,
		message TEXT,
		last_updated TEXT
		)""")
	db.commit()
	db.close()	

def init_cus_status(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE cus_status(
		ws_cust_id INTEGER NOT NULL PRIMARY KEY,
		ws_ssn INTEGER NOT NULL ,
		status TEXT,
		message TEXT,
		last_updated TEXT
		)""")
	db.commit()
	db.close()


def init_db_user_store(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE user_store(
		login_id text NOT NULL PRIMARY KEY,
		pass text,
		created_time text,
		type Text 
		)""")
	db.commit()
	db.close()


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
	db=get_db()
	cur=db.cursor()
	db.execute("DROP TABLE "+name)


def add_new_cus(**det):
	db=get_db()
	cur = db.cursor()
	try:
		cur.execute("INSERT INTO customers (ws_ssn,ws_name,ws_adrs,ws_age) VALUES (?,?,?,?)",
	    	(int(det["ws_ssn"]),det["ws_name"],det["ws_adrs"]+"#"+det["state"]+"#"+det["city"],int(det["ws_age"])))
		det["status"]="ACTIVE"
		det["message"]="customer created successfully"
		cur.execute("SELECT last_insert_rowid()")
		det["ws_cust_id"]=str(cur.fetchone()[0])
		if add_cus_status(det,db):
			db.commit()
			return True
		else:
			raise Exception ("NOT logged")	
	except Exception as e :
		db.rollback()
		print(e)
	finally:
		db.close()
	return False

def update_cus(**det):
	db=get_db()
	db.row_factory = dict_factory
	cur = db.cursor()
	updatable=["ws_name","ws_age","ws_adrs"]
	colunm_names=list(det.keys())
	try:
		for cn in colunm_names:
			if cn not in updatable:
				continue
			if cn=="ws_adrs":
				old_det=get_cus_det(**{"ws_cust_id":det["ws_cust_id"]})
				det["ws_adrs"]=det["ws_adrs"]+"#"+old_det["state"]+"#"+old_det["city"]
			cur.execute("UPDATE customers SET "+cn+" = ? where ws_cust_id = ?",(det[cn],det["ws_cust_id"]))
		log_dic={"message":"customer update complete",
					"last_updated":str(datetime.now()),
					"ws_cust_id":det["ws_cust_id"]}
		if update_cus_status(log_dic,db):	
			db.commit()
			return True
		else:
			raise Exception ("NOT logged")
	except Exception as e :
		db.rollback()
		print(e)
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
	finally:
		db.close()
	return False
         
def add_new_account(**det):
	db=get_db()
	cur = db.cursor()
	try:
		cur.execute("""INSERT INTO account (ws_cust_id,ws_acct_type,ws_acct_balance,ws_acct_crdate,ws_acct_lasttrdate)
		 VALUES (?,?,?,?,?)""",
		 (int(det["ws_cust_id"]),det["ws_acct_type"],float(det["ws_acct_balance"]),str(date.today()),str(date.today())))
		db.commit()
		return True
	except Exception as e :
		print(e)
		db.rollback()
	finally:
		db.close()
	return False

def get_account_det(**det):
	db=get_db()
	db.row_factory = dict_factory
	cur = db.cursor()
	acc_id=list(det.keys())[0]
	try:
		if acc_id=="ws_acct_id":
			cur.execute("SELECT * FROM account where "+acc_id+" = (?)",(int(det[acc_id]),))
			acc_det=cur.fetchone()
		elif acc_id=="ws_cust_id":
			cur.execute("SELECT * FROM account where ws_cust_id=(?)",(int(det["ws_cust_id"]),))
			acc_det=cur.fetchall()
		elif acc_id=="ws_ssn":
			cur.execute("SELECT ws_cust_id FROM customer where ws_ssn=(?)",(int(det["ws_ssn"]),))
			cust_id=fetchone()
			cur.execute("SELECT * FROM account where ws_cust_id=(?)",(int(det["ws_cust_id"]),))
			acc_det=cur.fetchall()
		else:	
			acc_det=None
		# print(customer_det)
		db.commit()
		return acc_det
	except Exception as e :
		db.rollback()
		print(e)
	finally:
		db.close()
	return False	

def del_account(**det):
	db=get_db()
	db.row_factory = dict_factory
	cur = db.cursor()
	try:
		account_det=get_account_det(**det)
		cur.execute("DELETE FROM account where ws_acct_id = (?)",(det["ws_acct_id"],))
		db.commit()
		return account_det
	except Exception as e :
		db.rollback()
		print(e)
	finally:
		db.close()
	return False

def get_cus_status(det=None):
	db=get_db()
	db.row_factory = dict_factory
	cur = db.cursor()
	try:
		if det==None:
			cur.execute("SELECT * FROM cus_status")
			status=cur.fetchall()
		else:
			cur.execute("SELECT * FROM cus_status where ws_cust_id=(?)",(det["ws_cust_id"],))
			status=cur.fetchone()
		db.commit()
		return status
	except Exception as e :
		db.rollback()
		print(e)
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
	d={"ws_acct_type":"S" ,"ws_acct_balance":"1230340","ws_cust_id":"7"}
	# add_new_user(get_db(),**d)
	# add_new_cus(**c)
	# init_db_customers()
	# update_cus(**c2)
	# print(get_cus_det(**{"ws_cust_id":2}))
	# add_new_account(**d)
	# print(get_account_det(**{"ws_cust_id":"2"}))
	# print(del_account(**{"ws_acct_id":"500000004"}))

