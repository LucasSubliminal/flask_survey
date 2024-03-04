from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def start_survey():
    title = survey.title
    instructions = survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route("/begin", methods=["POST"])
def start():
    session[RESPONSES_KEY] = []  
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    choice = request.form['answer']  

    responses = session.get(RESPONSES_KEY, [])
    
    responses.append(choice)

    session[RESPONSES_KEY] = responses

    if len(responses) >= len(survey.questions):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESPONSES_KEY, [])
    if qid >= len(survey.questions):
        return redirect("/complete")
    if qid != len(responses):
        flash("You're trying to access an invalid question. Please answer the questions in order.")
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[qid]
    return render_template('questions.html', question=question)
@app.route('/complete')
def complete_survey():
    return render_template('complete.html')
