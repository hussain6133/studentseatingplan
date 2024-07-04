from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize seats: A-V rows, 1-29 columns
rows = list("ABCDEFGHIJKLMNOPQRSTUV")
cols = list(range(1, 30))

# Create an in-memory data structure for seat reservations
seats = {f"{row}{col}": {"status": "available", "note": ""} for row in rows for col in cols}

# Track the last reservation for undo functionality
last_reservation = []

@app.route("/")
def index():
    return render_template("index.html", seats=seats, rows=rows, cols=cols)

@app.route("/reserve", methods=["POST"])
def reserve():
    global last_reservation
    seat_ids = request.json.get("seat_ids", [])
    note = request.json.get("note", "")
    last_reservation = []

    for seat_id in seat_ids:
        if seats[seat_id]["status"] == "available":
            seats[seat_id]["status"] = "reserved"
            seats[seat_id]["note"] = note
            last_reservation.append(seat_id)

    return jsonify(success=True)

@app.route("/cancel_last_reservation", methods=["POST"])
def cancel_last_reservation():
    global last_reservation
    for seat_id in last_reservation:
        seats[seat_id]["status"] = "available"
        seats[seat_id]["note"] = ""

    last_reservation = []

    return jsonify(success=True)

@app.route("/reset_all", methods=["POST"])
def reset_all():
    global seats
    for key in seats:
        seats[key]["status"] = "available"
        seats[key]["note"] = ""
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
