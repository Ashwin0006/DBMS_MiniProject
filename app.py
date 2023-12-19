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

@app.route("/cric_player_data", methods=['POST', 'GET'])
def cric_player_data():
    option = request.form['cricplayeroption']
    if option == "insert":
        p_id = request.form["field1"]
        p_name = request.form["field2"]
        t_id = request.form["field3"]
        j_no = request.form["field4"]
        no_played = request.form["field5"]
        
        query = f"INSERT INTO cricket_players VALUES ('{p_id}', '{p_name}', '{t_id}', '{j_no}', '{no_played}')"
        cursor.execute(query)
        cursor.execute('COMMIT')

        query = f"SELECT * FROM Cricket_Players WHERE team_id = {t_id}"
        cursor.execute(query)
        data = cursor.fetchall()
        return render_template("Cricket_player_details.html", players_data = data)
    if option == "delete":
        p_id = request.form["field1"]

        #Getting Team ID
        cursor.execute(f"SELECT DISTINCT team_id FROM Cricket_Players WHERE player_id = {p_id}")
        t_id = cursor.fetchall()
        print("THE TEAM ID IS :", t_id)

        query = f"DELETE FROM Cricket_Players WHERE player_id = {p_id}"
        cursor.execute(query)
        cursor.execute("COMMIT")

        query = f"SELECT * FROM Cricket_Players WHERE team_id = {t_id[0][0]}"
        cursor.execute(query)
        data = cursor.fetchall()
        return render_template("Cricket_player_details.html", players_data = data)
    return "Showing Player Data!"
if __name__ == "__main__":
    main()
    
    app.run(debug = True)
