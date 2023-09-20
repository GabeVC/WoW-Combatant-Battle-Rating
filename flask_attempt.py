# Import necessary modules
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
import main_program
from player import Player
import sys
import api  # Assuming you have the 'api' module

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app, origins="http://localhost:3000")


# Create a route to handle POST requests for processing data
@app.route("/process_data", methods=["POST"])
@cross_origin(supports_credentials=True)
def process_data():
    try:
        # Get the 'code' value from the JSON data sent by the frontend
        data = request.json
        code = data.get("reportCode")
        if data.get("action") == "BRUNT":
            return brunt_data(data)
        # Check for additional keys to determine the action

        # Call the main function and return its result
        result = main(code)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})


def brunt_data(data):
    try:
        id = int(data.get("id"))
        code = str(data.get("reportCode"))
        title = data.get("title")
        temp3 = main_program.create_players(id, code)
        if title == "Kazzara, the Hellforged":
            players = main_program.kazzara(code, id, temp3)
        elif title == "The Amalgamation Chamber":
            players = main_program.shadowflame(code, id, temp3)
        elif title == "Assault of the Zaqali":
            players = main_program.zaqali(code, id, temp3)
        elif title == "The Forgotten Experiments":
            players = main_program.experiments(code, id, temp3)
        elif title == "Rashok, the Elder":
            players = main_program.rashok(code, id, temp3)
        elif title == "The Vigilant Steward, Zskarn":
            players = main_program.zskarn(code, id, temp3)
        elif title == "Magmorax":
            players = main_program.magmorax(code, id, temp3)
        elif title == "Echo of Neltharion":
            players = main_program.neltharion(code, id, temp3)
        elif title == "Scalecommander Sarkareth":
            players = main_program.sarkareth(code, id, temp3)

        players.sort(key=lambda x: x.score, reverse=True)
        for player in players:
            print(player)
        players_data = [player.to_dict() for player in players]
        return jsonify(players_data)

    except Exception as e:
        return jsonify({"error": str(e)})


# Define the main function that processes data
def main(code):
    print(code)
    fights = api.get_fights(str(code))
    temp = []

    # Process fights and add them to the 'temp' list
    for fight in fights.items():
        temp.append((fight[0], fight[1]))
        print(fight)


    # Prepare and return the processed data as a dictionary
    processed_data = {
        "temp": temp,  # Include any relevant data here
    }
    print("Does it work here")
    return processed_data


# Run the Flask app if this script is run directly
if __name__ == "__main__":
    app.run()
