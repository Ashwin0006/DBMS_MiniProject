from flask import Flask, render_template, request
import cx_Oracle


cx_Oracle.init_oracle_client(lib_dir=r"E:\Database\DB\dbhomeXE\bin")
orcl_connec_str = 'system/ak@localhost:1521/XE'
connection = cx_Oracle.connect(orcl_connec_str)
cursor = connection.cursor()


def main():
    pass



# Main Flask App!
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/next_page", methods=["POST", "GET"])
def next_page():
    option = request.form["selectedGame"]
    if(option == "Cricket"):
        cursor.execute("SELECT * FROM Cricket_Teams")
        data = cursor.fetchall()
        return render_template("Cricket.html", teams_data = data)
    elif(option == "Football"):
        return render_template("FootBall.html")
    return "Error :Unable to Process Request!"

@app.route("/cric_data", methods=['POST', 'GET'])
def cric_data():
    option = request.form["cricoption"]
    if option == "insert":
        id = request.form["field1"]
        name = request.form["field2"]
        wins = request.form["field3"]
        query = f"INSERT INTO CRICKET_TEAMS VALUES ({id}, '{name}', 11, {wins})"
        cursor.execute(query)
        cursor.execute("Commit")
        cursor.execute("SELECT * FROM Cricket_Teams")
        data = cursor.fetchall()
        return render_template("Cricket.html", teams_data = data)
    elif option == "delete":
        id = request.form["field1"]
        query = f"DELETE FROM Cricket_Teams WHERE team_id = {id}"
        cursor.execute(query)
        cursor.execute("Commit")
        cursor.execute("SELECT * FROM Cricket_Teams")
        data = cursor.fetchall()
        return render_template("Cricket.html", teams_data = data)
    elif option == "get":
        id = request.form["field1"]
        query = f"SELECT * FROM CRICKET_PLAYERS WHERE team_id = {id}"
        cursor.execute(query)
        data = cursor.fetchall()
        return render_template("Cricket_player_details.html", players_data = data)

@app.route("/cric_player_data")
def cric_player_data():
    
if __name__ == "__main__":
    main()
    app.run(debug = True)