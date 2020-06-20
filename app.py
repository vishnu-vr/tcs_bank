from flask import Flask,request,render_template,redirect,url_for,make_response,jsonify,json,g,flash,session
import sql_func as sql
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "asdsad890asdashdlahdlj1n2j3bjk4bhkbj12n3jl1"

DATABASE = 'bank.db'

# sql.get_account_det(**{'customer_id':})

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db
#     # return sqlite3.connect(DATABASE)

# 
@app.route('/home')
def home():
    title="home".upper()
    return render_template('home.html',title=title)

@app.route('/Logout')
def Logout():
    session.pop('username', None)
    return redirect('/login',302)

# login
@app.route('/')
@app.route('/login',methods = ['POST', 'GET'])
def login():
    title = "login".upper()
    # render the page
    if request.method == 'GET':
        return render_template("login.html",error=0,title=title)

    # if login button pressed
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        session["username"] = request.form['username']
        
        data_from_db = sql.get_user(**{"login_id":username})
        # print(data_from_db)

        if data_from_db == None:
            return render_template("login.html",error="invalid user",title=title)
        elif data_from_db["pass"] == password:
            # return render_template("options.html")
            return redirect("/home",302)
        else:
            return render_template("login.html",error="password is incorrect",title=title)

        # res = make_response(jsonify(return_data),200)
        # return res

# get_single_account_detail
@app.route('/get_single_account_detail',methods=['POST'])
def get_single_account_detail():
    if request.method == 'POST':
        # print("asd")
        # create customer
        # account_details = {"customer_id":123123,
        # "account_id":123123123,
        # "account_type":"savings",
        # "balance":50}
        data_from_db = sql.get_account_det(**request.get_json())
        # print(data_from_db)
        # for i in range(10):
        #     print(0)
        # return_data = {"message":"account details fetched successfully"}
        if data_from_db:
            return make_response(jsonify(data_from_db),200)
        else:
            return make_response(jsonify({"message":"error"}),200)


# deposit money
@app.route('/deposit',methods=['POST'])
def deposit():
    if request.method == 'POST':
        if request.form['account_id']:
            return "deposit was clicked "+request.form['account_id']

# withdraw money
@app.route('/withdraw',methods=['POST'])
def withdraw():
    if request.method == 'POST':
        # print("asdasd")
        return "withdraw was clicked "+request.form['account_id']

# transfer money
@app.route('/transfer',methods=['POST'])
def transfer():
    if request.method == 'POST':
        # print("asdasd")
        return "transfer was clicked "+request.form['account_id']

# get account details
@app.route('/account_details',methods = ['POST', 'GET'])
def account_details():
    if 'username' not in session:
        return redirect("/login",302)
    title = "GET ACCOUNT DETAILS"

    if request.method == 'GET':
        return render_template("account_details.html",title=title)
    if request.method == 'POST':
        
        # print("asd")
        # create customer
        # data_from_db = [{'ws_cust_id': 2, 'ws_acct_id': 500000002, 'ws_acct_type': 'c', 'ws_acct_balance': 12300.0, 'ws_acct_crdate': '2020-06-18', 'ws_acct_lasttrdate': '2020-06-18'}, {'ws_cust_id': 2, 'ws_acct_id': 500000004, 'ws_acct_type': 'savings', 'ws_acct_balance': 123123.0, 'ws_acct_crdate': '2020-06-18', 'ws_acct_lasttrdate': '2020-06-18'}, {'ws_cust_id': 2, 'ws_acct_id': 500000005, 'ws_acct_type': 'savings', 'ws_acct_balance': 12312313.0, 'ws_acct_crdate': '2020-06-18', 'ws_acct_lasttrdate': '2020-06-18'}]
        # return_data = {"message":"account details fetched successfully"}
        data_to_send = {}
        # print(request.get_json())
        for key,value in request.get_json().items():
            if value != "":
                data_to_send[key] = value
        # print(data_to_send)
        # for i in range(10):
        #     print(0)
        data_from_db = sql.get_account_det(**data_to_send)
        if data_from_db:
            return make_response(jsonify(data_from_db),200)
        else:
            return make_response(jsonify({"message":"error"}),200)

@app.route('/account_status',methods=['POST','GET'])
def account_status():
	if 'username' not in session:
	    return redirect("/login",302)    
	title = "account_status".upper()

	# data_from_db = [{"ws_cust_id":"123123123",
	#                 "ws_accnt_type":"current",
	#                 "status":"active",
	#                 "message":"onnu poda mone",
	#                 "last_updated":"yesterday"},
	#                 {"ws_cust_id":"32131312",
	#                 "ws_accnt_type":"savings",
	#                 "status":"active",
	#                 "message":"onnu poda mone",
	#                 "last_updated":"yesterday"}]

	data_from_db = sql.get_account_status()
	# if method == get it should return details of all accounts present in the db
	if request.method == 'GET':
	    if data_from_db:
	        return render_template("account_status.html",customer_details=data_from_db,title=title)
	    else:
	        return render_template("account_status.html",message="error",customer_details=data_from_db,title=title)
	# single account update details
	if request.method == 'POST':
	    # data_from_db = {"ws_cust_id":"123",
	    #             "ws_accnt_type":"current",
	    #             "status":"deactivate",
	    #             "message":"onnu poda mone",
	    #             "last_updated":"today"}

	    data_from_db = sql.get_account_status(ws_acct_id=request.get_json()["ws_acct_id"])

	    # print(request.get_json())
	    # for i in range(10):
	    # 	print(0)

	    if data_from_db:
	        return make_response(jsonify(data_from_db),200)
	    else:
	        return make_response(jsonify({"message":"error"}),200)


@app.route('/customer_status',methods=['POST', 'GET'])
def customer_status():
    if 'username' not in session:
        return redirect("/login",302)
    title = "customer_status".upper()

    # data_from_db = [{"ws_cust_id":"123123123",
    #                 "ws_ssn":"12312313",
    #                 "status":"active",
    #                 "message":"onnu poda mone",
    #                 "last_updated":"yesterday"},
    #                 {"ws_cust_id":"32131312",
    #                 "ws_ssn":"12312313",
    #                 "status":"active",
    #                 "message":"onnu poda mone",
    #                 "last_updated":"yesterday"}]
    data_from_db = sql.get_cus_status()
    if request.method == 'GET':
        if data_from_db:
            return render_template("customer_status.html",customer_details=data_from_db,title=title)
        else:
            return render_template("customer_status.html",message="error",customer_details=data_from_db,title=title)
    # single update
    if request.method == 'POST':
        # data_from_db = {"ws_cust_id":"0",
        #             "ws_ssn":"0",
        #             "status":"deactivate",
        #             "message":"onnu poda mone",
        #             "last_updated":"yesterday"}
        data_from_db = sql.get_cus_status(request.get_json())
        if data_from_db:
            return make_response(jsonify(data_from_db),200)
        else:
            return make_response(jsonify({"message":"error"}),200)

# delete_account
@app.route('/delete_account',methods = ['POST', 'GET'])
def delete_account():
    if 'username' not in session:
        return redirect("/login",302)    
    title = "delete_account".upper()

    if request.method == 'GET':
        return render_template("delete_account.html",title=title)
    if request.method == 'POST':
        data_from_db = sql.del_account(**request.get_json())
        if data_from_db:
            return make_response(jsonify({"message":"“Account deletion initiated successfully”"}),200)
        else:
            return make_response(jsonify({"message":"error"}),200)

# create_account
@app.route('/create_account',methods = ['POST', 'GET'])
def create_account():
    if 'username' not in session:
        return redirect("/login",302)
    title = "create_account".upper()

    if request.method == 'GET':
        return render_template("create_account.html",title=title)
    if request.method == 'POST':
        data_from_db = 0
        data_from_db = sql.add_new_account(**request.get_json())
        if data_from_db:
            return make_response(jsonify({"message":"Account creation initiated successfully"}),200)
        else:
            return make_response(jsonify({"message":"error"}),200)

# create_customer
@app.route('/create_customer',methods = ['POST', 'GET'])
def create_customer():
    if 'username' not in session:
        return redirect("/login",302)    
    title = "create_customer".upper()

    if request.method == 'GET':
        return render_template("create_customer.html",title=title)
    if request.method == 'POST':
        if len(request.form["customer_ssn_id"]) != 9:
            print("ssn id error")
            return render_template("create_customer.html",message="ssn id should be 9 digits long",title=title)
        else:
            data_from_db = sql.add_new_cus(**{"ws_ssn":request.form["customer_ssn_id"],
                "ws_name":request.form["customer_name"],
                "ws_age":request.form["age"],
                "ws_adrs":request.form["address"],
                "state":request.form["state"],
                "city":request.form["city"]})

            if data_from_db:
                return render_template("create_customer.html",message="Customer creation initiated successfully",title=title)
            else:
                return render_template("create_customer.html",message="something went wrong!!! Maybe this customer already exist",title=title)

# get customer_details
@app.route('/customer_details',methods = ['POST'])
def customer_details():
    if 'username' not in session:
        return redirect("/login",302) 
    if request.method == 'POST':
        data_from_db = 0

        if request.get_json()["ws_ssn"] != "":
            data_from_db = sql.get_cus_det(**{"ws_ssn":request.get_json()["ws_ssn"]})
        else:
            data_from_db = sql.get_cus_det(**{"ws_cust_id":request.get_json()["ws_cust_id"]})

        if data_from_db:
            return make_response(jsonify(data_from_db),200)
        else:
            return make_response(jsonify({"message":"error"}),200)

# update_customer
@app.route('/update_customer',methods = ['POST', 'GET'])
def update_customer():
    if 'username' not in session:
        return redirect("/login",302)     
    title = "update_customer".upper()

    if request.method == 'GET':
        return render_template("update_customer.html",title=title)
    if request.method == 'POST':
        data_to_send = {}
        for key,value in request.get_json().items():
            if value != "":
                data_to_send[key] = value
        # print(data_to_send)
        data_from_db = sql.update_cus(**data_to_send)
        if data_from_db:
            return make_response(jsonify({"message":"Customer update initiated successfully"}),200)
        else:
            return make_response(jsonify({"message":"error"}),200)

# delete_customer
@app.route('/delete_customer',methods = ['POST', 'GET'])
def delete_customer():
    if 'username' not in session:
        return redirect("/login",302)     
    title = "delete_customer".upper()

    if request.method == 'GET':
        return render_template("delete_customer.html",title=title)
    if request.method == 'POST':
        data_from_db = sql.del_cus(**{"ws_cust_id":request.get_json()["ws_cust_id"]})
        if data_from_db:
            return make_response(jsonify({"message":"Customer deletion initiated successfully"}),200)
        else:
            return make_response(jsonify({"message":"error"}),200)

# get_info
@app.route('/get_customer_info',methods = ['POST'])
def get_customer_info():
    if 'username' not in session:
        return redirect("/login",302)     

    customer_ssn_id = None
    customer_id = None
    
    if request.is_json:
        data = request.get_json(force=True)
        if 'customer_ssn_id' in data:
            customer_ssn_id = data['customer_ssn_id']
            # query the database here
        elif 'customer_id' in data:
            customer_id = data['customer_id']
            # or from here

    # print(customer_id)
    # print(customer_ssn_id)

    return_data = {"message":"error"}

    # validate the customer
    valid_customer = 1
    if valid_customer:
        # return_data should be filled with data fetched form db
        return_data = {"old_age":60,"old_address":"berlin"}

    res = make_response(jsonify(return_data),200)

    return res

# if ssn is given i want all the account_ids belonging to that customer
@app.route('/get_all_account_ids',methods=['POST'])
def account_details_testing():
    if 'username' not in session:
        return redirect("/login",302) 
    if request.method == 'POST':
        data_to_send = {}
        # print(request.get_json())
        for key,value in request.get_json().items():
            if value != "":
                data_to_send[key] = value
        # print(data_to_send)

        # for i in range(10):
        #     print(0)

        data_from_db = sql.get_acc_names(**data_to_send)
        # data_from_db=0
        if data_from_db:
            return make_response(jsonify(data_from_db),200)
        else:
            return make_response(jsonify({"message":"error"}),200)


if __name__ == "__main__":
    app.run("localhost",1234,debug=True);











