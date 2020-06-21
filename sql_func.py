## the sql functions
import sqlite3
from flask import g,Flask
from datetime import date,datetime

# path='/Volumes/Macintosh HD/Users/vishnu/Desktop/tcs_bank/app'
# DATABASE = '/Volumes/Macintosh HD/Users/vishnu/Desktop/tcs_bank/app/bank.db'
DATABASE="bank.db"
tables = ["account","account_status","cus_status","customers","user_store"]

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
				str(datetime.now().replace(microsecond=0))
				))
		return True
	except Exception as e :
		print(e)
		db.rollback()
	return False

def update_acc_status(det,db):
	cur = db.cursor()
	updatable=["status","message","last_updated"]
	colunm_names=list(det.keys())
	try:
		for cn in colunm_names:
			if cn not in updatable:
				continue
			cur.execute("UPDATE account_status SET "+cn+" = ? where ws_acct_id = ?",(det[cn],det["ws_acct_id"]))
		return True
	except Exception as e :
		db.rollback()
		print(e)
	return False

def add_acc_status(det,db):
	# db=get_db()
	cur=db.cursor()	
	try:
		# print(det)
		cur.execute("INSERT INTO account_status (ws_cust_id,ws_acct_id,ws_acct_type,status,message,last_updated) VALUES (?,?,?,?,?,?)",
			(	int(det["ws_cust_id"]),
				int(det["ws_acct_id"]),
				det["ws_acct_type"],
				det["status"],
				det["message"],
				str(datetime.now().replace(microsecond=0))
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

def init_customers(db=get_db()):
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

def init_account(db=get_db()):
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

def init_transactions(cus_id,db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE transactions"""+str(cus_id)+""" (
		ws_acct_id INTEGER NOT NULL,
		ws_acct_type TEXT,
		ws_trxn_date TEXT,
		ws_trxn_type TEXT,
		ws_amt INTEGER,
		ws_acct_balance REAL
		)""")
	return True

def init_account_status(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE account_status(
		ws_cust_id INTEGER NOT NULL ,
		ws_acct_id INTEGER NOT NULL PRIMARY KEY,
		ws_acct_type text,
		status TEXT,
		message TEXT,
		last_updated TEXT
		)""")
	db.commit()

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

def init_user_store(db=get_db()):
	cur=db.cursor()
	cur.execute("""CREATE TABLE user_store(
		login_id text NOT NULL PRIMARY KEY,
		pass text,
		created_time text,
		type Text 
		)""")
	db.commit()

def init_tables(db=get_db()):
	cur=db.cursor()
	global tables
	try:
		cur.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
		fetched_tables=[item[0] for item in cur.fetchall()]
		# print(fetched_tables)
		for items in tables:
			if items not in fetched_tables:
				eval("init_"+items+"(db)")
		db.commit()
	except Exception as e:
		print(e)
		db.rollback()
		db.close()
		return False
	finally:
		db.close()
	return True

def get_user(**det):
	db=get_db()
	db.row_factory = dict_factory
	cur=db.cursor()
	cur.execute("SELECT * FROM user_store where login_id = (?)",(det["login_id"],))
	user=cur.fetchone()
	db.close()
	return user

def add_new_user(**det):
	db=get_db()
	cur = db.cursor()
	cur.execute("INSERT INTO user_store VALUES (?,?,?,?)",(det["login_id"],det["pass"],str(date.today()),det["type"]))
	db.commit()
	db.close()
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
		if add_cus_status(det,db) and init_transactions(det["ws_cust_id"],db):
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
					"last_updated":str(datetime.now().replace(microsecond=0)),
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
		cur.execute("SELECT * from account where ws_cust_id = (?)",(det["ws_cust_id"],))
		accs=cr.fetchall()
		cur.execute("DELETE FROM customers where ws_cust_id = (?)",(det["ws_cust_id"],))
		for items in accs:
			cur.execute("DELETE FROM account where ws_acct_id = (?)",(items["ws_acct_id"],))
			det1={"message":"Account deleted",
				"status":"DEACTIVE",
				"last_updated":str(datetime.now().replace(microsecond=0)),
				"ws_acct_id":items["ws_acct_id"]
			}
			if update_acc_status(det1,db)==False:
				raise Exception("Not logged")
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
		cur.execute("SELECT * from customers where ws_cust_id=(?)",(det["ws_cust_id"],))
		if cur.fetchone()==None:
			raise Exception ("no such customer")
		cur.execute("""INSERT INTO account (ws_cust_id,ws_acct_type,ws_acct_balance,ws_acct_crdate,ws_acct_lasttrdate)
		 VALUES (?,?,?,?,?)""",
		 (int(det["ws_cust_id"]),det["ws_acct_type"],float(det["ws_acct_balance"]),
		 	str(datetime.now().replace(microsecond=0)),str(datetime.now().replace(microsecond=0))))
		cur.execute("SELECT last_insert_rowid()")
		det["ws_acct_id"]=str(cur.fetchone()[0])
		det["status"]="ACTIVE"
		det["message"]="Account creation complete"
		det["transaction_type"]="Deposited"
		det["ws_amt"]=det["ws_acct_balance"]
		if add_acc_status(det,db) and add_trans(det,db):
			db.commit()
			return True
		else:
			raise Exception ("NOT logged")
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
		if acc_id == "all":
			cur.execute("SELECT * from account")
			acc_det=cur.fetchall()
		if acc_id == "ws_acct_id":
			cur.execute("SELECT * FROM account where "+acc_id+" = (?)",(int(det[acc_id]),))
			acc_det=cur.fetchone()
		elif acc_id == "ws_cust_id":
			cur.execute("SELECT * FROM account where ws_cust_id=(?)",(int(det["ws_cust_id"]),))
			acc_det=cur.fetchall()
		elif acc_id =="ws_ssn":
			cur.execute("SELECT ws_cust_id FROM customers where ws_ssn=(?)",(int(det["ws_ssn"]),))
			cust_id=cur.fetchone()
			cur.execute("SELECT * FROM account where ws_cust_id=(?)",(int(cust_id["ws_cust_id"]),))
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
	db.row_factory = dict_factory
	cur = db.cursor()
	try:
		account_det=get_account_det(**det)
		cur.execute("DELETE FROM account where ws_acct_id = (?)",(det["ws_acct_id"],))
		det={"message":"Account deleted","status":"DEACTIVE","last_updated":str(datetime.now().replace(microsecond=0))}
		if update_acc_status(det,db):
			db.commit()
			return account_det
		else:
			raise Exception("Not logged")
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
	
def get_account_status(**det):
	db=get_db()
	db.row_factory = dict_factory
	cur = db.cursor()
	try:
		if "ws_acct_id" not in det.keys():
			cur.execute("SELECT * FROM account_status")
			status=cur.fetchall()
		else:
			cur.execute("SELECT * FROM account_status where ws_acct_id=(?)",(det["ws_acct_id"],))
			status=cur.fetchone()
		db.commit()
		db.close()
		return status
	except Exception as e :
		db.rollback()
		print(e)
	finally:
		db.close()
	return False

def get_acc_names(**det):
	acc_det=get_account_det(**det)
	# print(acc_det)
	if acc_det != False:
		l=[]
		for i in acc_det:
			l.append(i["ws_acct_id"])
		return l
	else:
		return False

def update_bal(det,db=get_db()):
	cur=db.cursor()
	try:
		cur.execute("SELECT ws_acct_balance,ws_acct_type,ws_cust_id from account where ws_acct_id=(?)",(int(det["ws_acct_id"]),))
		old_det=cur.fetchone()
		old_bal=old_det[0]
		if det["transaction_type"] == "credited":
			bal=old_bal+float(det["amount"])
		else:
			bal=old_bal-float(det["amount"])
			if bal<0:
				return "Not enough balance in account"
		cur.execute("UPDATE account set ws_acct_balance=(?),ws_acct_lasttrdate=(?) where ws_acct_id =(?)",
			((bal),(str(datetime.now().replace(microsecond=0))),(int(det["ws_acct_id"]))))
		det2={	"ws_acct_id":det["ws_acct_id"],
				"ws_acct_type":old_det[1] ,
				"ws_cust_id":old_det[2],
				"transaction_type":det["transaction_type"] ,
				"ws_amt":det["amount"] ,
				"ws_acct_balance":bal
			}
		det1={"message":"Amount "+det["transaction_type"],
				"ws_acct_id":det["ws_acct_id"],
				"last_updated":(str(datetime.now().replace(microsecond=0))),
			}
		if update_acc_status(det1,db) and add_trans(det2,db):
			return True	
		else:
			raise Exception ("not logged")
	except Exception as e:
		print (e)
	return False

def check_acct_exist(db=get_db(),**det):
	cur=db.cursor()
	try:
		cur.execute("SELECT * from account where ws_acct_id=(?)",(det["ws_acct_id"],))
		res=cur.fetchone()
		if res==None:
			return False
		else :
			return True
	except Exception as e:
		print(e)
	return False

def transact(**det):
	db=get_db()
	data_req=["amount","transaction_type"]
	if det["transaction_type"]=="transfer":
		data_req+=["to_ws_acct_id","from_ws_acct_id"]
	else:
		data_req+=["ws_acct_id"]
	try:
		keys=det.keys()
		# print(keys,data_req)
		for item in data_req:
			if item not in keys:
				raise Exception ("Details not provided")		
		if det["transaction_type"] == "deposit":
			if check_acct_exist(db,ws_acct_id=det["ws_acct_id"])==False:
				raise Exception ("No such account")
			res=update_bal({"amount":det["amount"],"transaction_type":"credited","ws_acct_id":det["ws_acct_id"]},db)
		elif det["transaction_type"] == "withdraw":
			if check_acct_exist(db,ws_acct_id=det["ws_acct_id"])==False:
				raise Exception ("No such account")
			res=update_bal({"amount":det["amount"],"transaction_type":"debited","ws_acct_id":det["ws_acct_id"]},db)
		elif det["transaction_type"] == "transfer":
			if check_acct_exist(db,ws_acct_id=det["from_ws_acct_id"])==False or check_acct_exist(db,ws_acct_id=det["to_ws_acct_id"])==False :
				raise Exception ("No such account")
			res=update_bal({"amount":det["amount"],"transaction_type":"transfered","ws_acct_id":det["from_ws_acct_id"]},db)
			if res == True:
				res=update_bal({"amount":det["amount"],"transaction_type":"credited","ws_acct_id":det["to_ws_acct_id"]},db)
		else:
			raise Exception("function not defined")
		if res == True:
			db.commit()
			db.close()
			return True
		elif res == "Not enough balance in account":
			db.rollback()
			db.close()
			return res
		else:
			raise Exception ("Something went wrong at transaction")
	except Exception as e:
		print (e)
		db.rollback()
		db.close()
	finally:
		db.close()
	return False

def add_trans(det,db=get_db()):
	cur=db.cursor()
	try:
		tb=str(det["ws_cust_id"])
		cur.execute("INSERT INTO transactions"+tb+" VALUES(?,?,?,?,?,?)",(
				det["ws_acct_id"],
				det["ws_acct_type"] ,
				str(datetime.now().replace(microsecond=0)),
				det["transaction_type"] ,
				float(det["ws_amt"]) ,
				float(det["ws_acct_balance"])
			))
		return True
	except Exception as e:
		print(e)
	return False

def get_statement(**det):
	db=get_db()
	db.row_factory = dict_factory
	cur = db.cursor()
	try:
		if check_acct_exist(db,ws_acct_id=det["ws_acct_id"])==False:
				raise Exception ("No such account")
		cur.execute("SELECT ws_cust_id from account where ws_acct_id=(?)",(int(det["ws_acct_id"]),))
		tb="transactions"+str(cur.fetchone()["ws_cust_id"])
		if "nos" in det.keys():
			cur.execute("SELECT * from "+tb+" where ws_acct_id=(?) order by ws_trxn_date desc;",(int(det["ws_acct_id"]),))
			statements=cur.fetchmany(int(det["nos"]))
		elif "from_ws_trxn_date" in det.keys():
			cur.execute("SELECT * from "+tb+" where ws_acct_id=(?) and ws_trxn_date between (?) and (?) order by ws_trxn_date;",
				((int(det["ws_acct_id"])),(det["from_ws_trxn_date"]+" 00:00:00"),(det["to_ws_trxn_date"]+" 23:59:59"))
				)
			statements=cur.fetchall()
		else:
			cur.execute("SELECT * from "+tb+" where ws_acct_id=(?)",(int(det["ws_acct_id"]),))
			statements=cur.fetchall()
		db.commit()
		db.close()
		return statements
	except Exception as e :
		db.rollback()
		print(e)
	finally:
		db.close()
	return False


init_tables()
if __name__=='__main__':
	# init_db()
	# init_db_user_store()
	usr={
	"login_id":"test",
	"pass":"test",
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
	# add_new_user(**usr)
	t={"transaction_type":"transfer","amount":"1000","to_ws_acct_id":"500000001","from_ws_acct_id":"500000002"}
	# print(transact(**t))
	# get_account_status(ws_acct_id="500000002")
	# res=get_statement(ws_acct_id="500000001")#,from_ws_trxn_date="2020-06-21",to_ws_trxn_date="2020-06-22")
	# print(*res,sep="\n")

	det1={"ws_acct_id":"500000001","from_ws_trxn_date":"2020-06-21","to_ws_trxn_date":"2020-06-22"}
	det2={"ws_acct_id":"500000001","nos":"5"}
	det3={"ws_acct_id":"500000001"}
	res=get_statement(**det3)
	print(*res,sep="\n")
		

