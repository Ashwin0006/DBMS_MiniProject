from flask import Flask, render_template, request
import cx_Oracle


app = Flask(__name__)
table_name = ''
data = []

cx_Oracle.init_oracle_client(lib_dir="E:/Database/DB/dbhomeXE/bin")
oracle_connection_string = 'system/ak@localhost:1521/XE'

connection = cx_Oracle.connect(oracle_connection_string)
cursor = connection.cursor()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/next-page", methods=["GET", "POST"])
def next_page():
    global data, table_name
    final = "Fatal Error!\nPlease Contact Developers"
    try:
        if request.method == "POST":
            selected_game = request.form['selectedGame']
            if(selected_game == "Cricket"):  
                query = "SELECT * FROM Cricket_Teams"   
                cursor.execute(query)
                result = cursor.fetchall() 
                print(result)
                data = result
                table_name = selected_game
                final = render_template("Cricket.html", results = result)
                return final
            elif(selected_game == "FootBall"):
                return render_template("FootBall.html", results = result)
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "INVALID REQUEST"

@app.route("/cric_data", methods=["post", "get"])
def cric_data():
    return "CRIC_DATA SUCCESSFUL...."

if __name__ == "__main__":
    app.run(debug=True)
