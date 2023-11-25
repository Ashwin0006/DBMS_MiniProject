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
                data = result
                table_name = "Cricket_Teams"
                final = render_template("Cricket.html", results = result)
                return final
            elif(selected_game == "FootBall"):
                return render_template("FootBall.html", results = result)
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "INVALID REQUEST!"

@app.route("/cric_data", methods=["POST", "GET"])
def cric_data():
    global table_name
    try:
        if not table_name:
            return render_template("index.html")
        if request.method == "POST":
            option = request.form['cricoption']
            if(option == "insert"):
                name = request.form['field1']
                color = request.form['field2']
                query = f"INSERT INTO {table_name} Values ('{name}', '{color}')"
                cursor.execute(query)
            elif(option == "delete"):
                name = request.form['field3']
                query = f"DELETE FROM {table_name} WHERE team_name = '{name}'"
                print(query)
                cursor.execute(query)
            elif(option == "get"):
                team = request.form['field4']
                query = f"SELECT PLAYER_ID, PLAYER_NAME, STATUS FROM Cricket_Team_Players WHERE TEAM_NAME = '{team}'"
                cursor.execute(query)
                result = cursor.fetchall()
                return render_template('Cricket_2.html', results = result)
            else:
                return "NOT A VALID OPTION"
            
            cursor.execute("SELECT * FROM Cricket_Teams")
            result = cursor.fetchall() 
            final = render_template("Cricket.html", results = result)

            connection.commit()

            return final    
    except Exception as e:
        return f"Error : {e}"
    return "INVALID REQUEST!"

if __name__ == "__main__":
    app.run(debug=True)
