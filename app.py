from flask import Flask, render_template, request
import pickle
import datahandler



# Defining Paths
mentor_path = r"data\mentor.pickle"
mentee_path = r"data\mentee.pickle"

# Defining helper functions
def read_data(path):
    data = None
    with open(path, 'rb') as infile:
        data = pickle.load(infile)
    return data

def check_cred(arr, user, pwd):
    flag = False
    for person in arr:
        if person.name == user and str(person.pwd) == str(pwd):
            flag = True
            break
    return flag

# Main Flask App!
app = Flask(__name__)
<<<<<<< HEAD
table_name = ''
data = []

cx_Oracle.init_oracle_client(lib_dir="E:/Database/DB/dbhomeXE/bin")
oracle_connection_string = 'system/ak@localhost:1521/XE'

connection = cx_Oracle.connect(oracle_connection_string)
cursor = connection.cursor()

#cursor.execute(f'START "ScriptSQL.sql"')

=======
>>>>>>> origin/main

@app.route("/")
def index():
    return render_template("Welcome.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    #try:
    if request.method == "POST":
        user = request.form['username']
        pwd = request.form['password']
        role = request.form['selectedRole']
        if role == "Mentor":
            data = read_data(mentor_path)
        elif role == "Student":
            data = read_data(mentee_path)
        access = check_cred(data, user, pwd)
        if access:
            return "Login Successful"
        else:
            return "Invalid Login"
    #except Exception as e:
        #return f"Error :{e}"
    return "Done!"

@app.route("/signup_page")
def signup_page():
    return render_template('Signup.html')

@app.route("/signup", methods=["POST", "GET"])
def signup():
    return "SignUp Successful!"

if __name__ == "__main__":
    app.run(debug = True)