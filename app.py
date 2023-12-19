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
    try:
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
    except Exception as e:
        return f"Error : {e}"

@app.route("/cric_player_data", methods=['POST', 'GET'])
def cric_player_data():
    try:
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
    except Exception as e:
        return f"Error :{e}"

@app.route("/go_to_tournaments")
def go_to_tournaments():
    try:
        query = "SELECT * FROM Cricket_Tournaments"
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        return render_template('Tournaments_display.html', tournament_data = data)
    except Exception as e:
        return f"Error : {e}"
@app.route("/make_change_to_tournaments", methods=["POST", "GET"])
def make_change_to_tournaments():
    try:
        option = request.form["tournamentoption"]
        if option == "insert":
            id_info = request.form["field1"]
            name = request.form["field2"]
            winner = request.form["field3"]
            total = request.form["field4"]
            
            query = f"INSERT INTO Cricket_Tournaments VALUES ('{id_info}', '{name}', '{winner}', '{total}')"
            cursor.execute(query)
            cursor.execute("COMMIT")

            cursor.execute('SELECT * FROM Cricket_Tournaments')
            results = cursor.fetchall()

            return render_template('Tournaments_display.html', tournament_data = results)
        elif option == "viewData":
            query = "SELECT * FROM Cricket_Games"
            cursor.execute(query)
            data_set = cursor.fetchall()

            new_data_set = []
            for data in data_set:
                new_data = []
                for j in range(len(data)):
                    result = data[j]
                    if(j == 1):
                        # Tournament id
                        input_variable = data[1]
                        result = cursor.callfunc("find_tournament_name", cx_Oracle.STRING, [input_variable])
                    elif(j == 2 or j == 3 or j == 4):
                        input_variable = data[j]
                        result = cursor.callfunc("find_team_name", cx_Oracle.STRING, [input_variable])
                    new_data.append(result)
                new_data_set.append(new_data)

            return render_template('cricket_games_paired.html', data_set = new_data_set)
    except Exception as e:
        return f"Error :{e}"

if __name__ == "__main__":
    main()
    
    app.run(debug = True)
