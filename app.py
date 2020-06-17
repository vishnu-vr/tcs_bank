from flask import Flask,request,render_template,redirect,url_for,make_response,jsonify,json,g,flash
import sql_func as sql
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "asdsad890asdashdlahdlj1n2j3bjk4bhkbj12n3jl1"

DATABASE = 'bank.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
    # return sqlite3.connect(DATABASE)

# home
@app.route('/')
def home():
    return "SEREVER UP!!!"

# login
@app.route('/login',methods = ['POST', 'GET'])
def login():
    # render the page
    if request.method == 'GET':
        return render_template("login.html",error=0)

    # if login button pressed
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        data_from_db = sql.get_user(db,**{"login_id":username})
        # print(data_from_db)

        if data_from_db == None:
            return render_template("login.html",error="invalid user")
        elif data_from_db["pass"] == password:
            return render_template("options.html")
        else:
            return render_template("login.html",error="password is incorrect")

        # res = make_response(jsonify(return_data),200)
        # return res

# get_single_account_detail
@app.route('/get_single_account_detail',methods=['POST'])
def get_single_account_detail():
    if request.method == 'POST':
        # print("asd")
        # create customer
        account_details = {"customer_id":123123,
        "account_id":123123123,
        "account_type":"savings",
        "balance":50}
        # return_data = {"message":"account details fetched successfully"}
        res = make_response(jsonify(account_details),200)
        return res

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
    if request.method == 'GET':
        return render_template("account_details.html")
    if request.method == 'POST':
        # print("asd")
        # create customer
        account_details = [123,456,789]
        # return_data = {"message":"account details fetched successfully"}
        res = make_response(jsonify(account_details),200)
        return res

# delete_account
@app.route('/delete_account',methods = ['POST', 'GET'])
def delete_account():
    account_numbers = [1,2,3]
    account_types = ["savings","current","savings"]
    details=dict(zip(account_numbers,account_types))
    if request.method == 'GET':
        return render_template("delete_account.html",details=details)
    if request.method == 'POST':
        if request.form["account_id"] == "None":
            return render_template("delete_account.html",details=details,message="select any of the account")
        else:
            return render_template("delete_account.html",details=details,message="account deleted")

# create_account
@app.route('/create_account',methods = ['POST', 'GET'])
def create_account():
    if request.method == 'GET':
        return render_template("create_account.html")
    if request.method == 'POST':
        return render_template("create_account.html",message="account created")


# create_customer
@app.route('/create_customer',methods = ['POST', 'GET'])
def create_customer():
    if request.method == 'GET':
        return render_template("create_customer.html")
    if request.method == 'POST':
        if len(request.form["customer_ssn_id"]) != 9:
            print("ssn id error")
            return render_template("create_customer.html",message="ssn id should be 9 digits long")
        else:
            # db = get_db()
            # data_from_db = sql.add_new_cus(db,**{"ws_ssn":request.form["customer_ssn_id"],
            #     "ws_name":request.form["customer_name"],
            #     "ws_age":request.form["age"],
            #     "ws_adrs":request.form["address"],
            #     "state":request.form["state"],
            #     "city":request.form["city"]})
            print({"ws_ssn":request.form["customer_ssn_id"],
                "ws_name":request.form["customer_name"],
                "ws_age":request.form["age"],
                "ws_adrs":request.form["address"],
                "state":request.form["state"],
                "city":request.form["city"]})
            return render_template("create_customer.html",message="customer created")

# update_customer
@app.route('/update_customer',methods = ['POST', 'GET'])
def update_customer():
    details = {"customer_ssn_id" : 123123123123,
        "customer_id" : 123123123,
        "old_customer_name" : "vishnu",
        "old_age" : 21,
        "old_address" : "palace road"}
    if request.method == 'GET':
        return render_template("update_customer.html",details=details)
    if request.method == 'POST':
        return render_template("update_customer.html",message="customer details updated",details=details)

# delete_customer
@app.route('/delete_customer',methods = ['POST', 'GET'])
def delete_customer():
    if request.method == 'GET':
        details = {"customer_ssn_id" : 123123123123,
        "customer_id" : 123123123,
        "customer_name" : "vishnu",
        "age" : 21,
        "address" : "palace road"}
        return render_template("delete_customer.html",details=details)
    if request.method == 'POST':
        return "redirect this to any previous page"

# get_info
@app.route('/get_customer_info',methods = ['POST'])
def get_customer_info():

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


if __name__ == "__main__":
    app.run("localhost",1234,debug=True);











