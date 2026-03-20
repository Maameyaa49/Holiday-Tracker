from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# creating a dictionary to store the holidays
# destination data base
destination_db = []


def load_destinations():
    if os.path.exists("destinations.json"):
        with open("destinations.json", "r") as f:
            return json.load(f)
    return []


def save_destinations(destination_db):
    with open("destinations.json", "w") as f:
        json.dump(destination_db, f)


destination_db = load_destinations()


@app.route("/")
def home():
    return render_template("index.html", destinations=destination_db)


# request is sending data to flask
#  so if the user is sending data to flask add it to the destination database and then send them back to the home page
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        destination = {
            "city": request.form["city"],
            "country": request.form["country"],
            "date": request.form["date"],
            "status": request.form["status"],
            "notes": request.form["notes"],
        }
        destination_db.append(destination)
        save_destinations(destination_db)
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/upcoming")
def upcoming():
    return render_template("upcoming.html", destinations=destination_db)


@app.route("/dream")
def dream():
    return render_template("dream.html", destinations=destination_db)


@app.route("/past")
def past():
    return render_template("past.html", destinations=destination_db)


@app.route("/delete/<int:index>")
def delete(index):
    destination_db.pop(index)
    save_destinations(destination_db)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
