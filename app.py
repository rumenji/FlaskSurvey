from flask import Flask, render_template, request, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
# debug = DebugToolbarExtension(app)

# RESPONSES = []

@app.route('/')
def start_survey():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/set_session', methods = ['POST'])
def set_session():
    session['responses'] = []
    return redirect ('/questions/0')

@app.route('/questions/<int:question_id>')
def questions(question_id):
    questions_list = satisfaction_survey.questions
    responses = session.get('responses')
    if len(responses) < len(questions_list):
        if question_id == len(responses):
            return render_template('question.html', question=questions_list[question_id], question_id=question_id)
        else:
            flash("You need to answer the questions in order!", 'error')
            return render_template('question.html', question=questions_list[len(responses)], question_id=len(session['responses']))
    else:    
        return redirect('/endsurvey')
    
    
@app.route('/answer', methods = ['POST'])
def answers():
    # import pdb
    # pdb.set_trace()
    answer = request.form['answer']
    next_question = request.form['id']
    responses = session.get('responses')
    responses.append(answer)
    session['responses'] = responses
    return redirect(f'questions/{int(next_question)+1}')

@app.route('/endsurvey')
def end_survey():
    return render_template('thanks.html')