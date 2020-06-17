from flask import Flask,request,render_template,redirect,url_for,make_response,jsonify,json
import sql_func as sql

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "asdsad890asdashdlahdlj1n2j3bjk4bhkbj12n3jl1"

# home
@app.route('/')
def home():
    return "SEREVER UP!!!"

# login
@app.route('/login',methods = ['POST', 'GET'])
def login():
    # render the page
    if request.method == 'GET':
        return render_template("login.html")

    # if login button pressed
    if request.method == 'POST':
        username = request.get_json()['username']
        password = request.get_json()['password']
        # print(username)
        return_data = {"message":"logged in successfully"}
        res = make_response(jsonify(return_data),200)
        return res

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
    if request.method == 'GET':
        account_numbers = [1,2,3]
        account_types = ["savings","current","savings"]
        details=dict(zip(account_numbers,account_types))
        return render_template("delete_account.html",details=details)
    if request.method == 'POST':
        # print("asd")
        # create customer
        return_data = {"message":"account deleted successfully"}
        res = make_response(jsonify(return_data),200)
        return res

# create_account
@app.route('/create_account',methods = ['POST', 'GET'])
def create_account():
    if request.method == 'GET':
        return render_template("create_account.html")
    if request.method == 'POST':
        # print("asd")
        # create customer
        return_data = {"message":"account created successfully"}
        res = make_response(jsonify(return_data),200)
        return res


# create_customer
@app.route('/create_customer',methods = ['POST', 'GET'])
def create_customer():
    if request.method == 'GET':
        return render_template("create_customer.html")
    if request.method == 'POST':
        # print("asd")
        # create customer
        return_data = {"message":"customer created successfully"}
        res = make_response(jsonify(return_data),200)
        return res

# update_customer
@app.route('/update_customer',methods = ['POST', 'GET'])
def update_customer():
    if request.method == 'GET':
        details = {"customer_ssn_id" : 123123123123,
        "customer_id" : 123123123,
        "old_customer_name" : "vishnu",
        "old_age" : 21,
        "old_address" : "palace road"}
        return render_template("update_customer.html",details=details)
    if request.method == 'POST':
        # print("asd")
        # create customer
        return_data = {"message":"updated successfully"}
        res = make_response(jsonify(return_data),200)
        return res

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
        # print(request.get_json())
        # create customer
        return_data = {"message":"deleted successfully"}
        res = make_response(jsonify(return_data),200)
        return res

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











