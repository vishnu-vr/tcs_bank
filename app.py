from flask import Flask,request,render_template,redirect,url_for,make_response,jsonify,json

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
        return render_template("update_customer.html")
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
        return render_template("delete_customer.html")
    if request.method == 'POST':
        # print("asd")
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











