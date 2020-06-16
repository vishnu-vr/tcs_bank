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
    # validate login
	return render_template("login.html")

# create_customer
@app.route('/create_customer')
def create_customer():
	return render_template()

# update_customer
@app.route('/update_customer')
def update_customer():
	return render_template("update_customer.html")

# get_info
@app.route('/get_info',methods = ['POST', 'GET'])
def get_info():

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

    print(customer_id)
    print(customer_ssn_id)

    # return_data should be filled with data fetched form db
    return_data = {"old_age":60,"old_address":"berlin"}

    res = make_response(jsonify(return_data),200)

    return res


if __name__ == "__main__":
    app.run("localhost",1234,debug=True);











