from flask import Flask, render_template, request, redirect
import random
import json

app = Flask(__name__)

number = random.randint(1,10)
attempts = 0


def load_scores():
    try:
        with open("players.json","r") as f:
            return json.load(f)
    except:
        return []


def save_score(name, difficulty, score):
    data = load_scores()

    data.append({
        "name": name,
        "difficulty": difficulty,
        "score": score
    })

    data = sorted(data, key=lambda x: x["score"])

    with open("players.json","w") as f:
        json.dump(data[:10], f)


@app.route("/", methods=["GET","POST"])
def index():

    global attempts, number

    message = ""

    if request.method == "POST":

        guess = int(request.form.get("guess",0))
        name = request.form.get("name")
        difficulty = request.form.get("difficulty")

        attempts += 1

        if guess == number:
            return render_template(
                "index.html",
                message="Correct!",
                win=True,
                attempts=attempts,
                name=name,
                difficulty=difficulty
            )

        elif guess < number:
            message = "Too low"

        else:
            message = "Too high"

    return render_template("index.html", message=message, attempts=attempts)


@app.route("/save", methods=["POST"])
def save():

    name = request.form.get("name")
    difficulty = request.form.get("difficulty")
    score = int(request.form.get("score"))

    save_score(name, difficulty, score)

    return redirect("/leaderboard")


@app.route("/leaderboard")
def leaderboard():

    players = load_scores()

    return render_template("leaderboard.html", players=players)


@app.route("/restart")
def restart():

    global number, attempts

    number = random.randint(1,10)
    attempts = 0

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)