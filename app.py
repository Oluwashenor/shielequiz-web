from flask import Flask, redirect, render_template, request, session, url_for

from questions import QUESTIONS

app = Flask(__name__)
app.secret_key = "shielequiz-dev-key"

CHOICES = ("A", "B", "C", "D")


def _reset_quiz():
    session["index"] = 0
    session["score"] = 0


@app.route("/")
def home():
    return render_template("home.html", total=len(QUESTIONS))


@app.post("/start")
def start():
    _reset_quiz()
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    index = session.get("index")
    if index is None:
        return redirect(url_for("home"))

    if index >= len(QUESTIONS):
        return redirect(url_for("result"))

    question = QUESTIONS[index]

    if request.method == "POST":
        answer = (request.form.get("answer") or "").upper()
        if answer not in CHOICES:
            return render_template(
                "quiz.html",
                question=question,
                number=index + 1,
                total=len(QUESTIONS),
                error="Please choose A, B, C, or D.",
            )

        if answer == question["correct_answer"]:
            session["score"] = session.get("score", 0) + 1

        session["index"] = index + 1
        if session["index"] >= len(QUESTIONS):
            return redirect(url_for("result"))
        return redirect(url_for("quiz"))

    return render_template(
        "quiz.html",
        question=question,
        number=index + 1,
        total=len(QUESTIONS),
        error=None,
    )


@app.get("/result")
def result():
    if "score" not in session:
        return redirect(url_for("home"))

    score = session.get("score", 0)
    total = len(QUESTIONS)
    session.clear()
    return render_template("result.html", score=score, total=total)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
