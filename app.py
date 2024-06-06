from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Load the questions CSV file
questions_df = pd.read_csv('modified_question.csv')

current_round = 0
correct_answers = 0
questions_order = []
player_name = None

def reset_game():
    global current_round, correct_answers, questions_order
    current_round = 0
    correct_answers = 0
    questions_order = list(range(len(questions_df)))
    random.shuffle(questions_order)

def get_current_question():
    global current_round
    question_index = questions_order[current_round]
    current_question = questions_df.iloc[question_index]
    question_text = current_question['Question']
    options = [current_question['A'], current_question['B'], current_question['C'], current_question['D']]
    random.shuffle(options)  # Shuffle the options for randomness
    return question_text, options

@app.route('/')
def index():
    reset_game()
    return render_template('index.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    global current_round, correct_answers, player_name
    if request.method == 'POST':
        user_answer = request.form.get('answer')  # Get the selected answer from the form
        correct_answer = questions_df.iloc[questions_order[current_round]]['Answer']
        if user_answer == correct_answer:
            correct_answers += 1
        current_round += 1
        if current_round == 10:  # Limit to 10 questions
            return redirect(url_for('result'))
    if current_round < len(questions_order) and current_round < 10:  # Limit to 10 questions
        question_text, options = get_current_question()
        return render_template('question.html', question_text=question_text, options=options, player_name=player_name)
    else:
        reset_game()
        return redirect(url_for('result'))

@app.route('/result')
def result():
    global correct_answers, player_name
    final_score = correct_answers
    reset_game()  # Reset game variables for new gamee
    return render_template('result.html', final_score=final_score, player_name=player_name)


@app.route('/set_name', methods=['POST'])
def set_name():
    global player_name
    player_name = request.form.get('username')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
