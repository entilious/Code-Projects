from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Location questions and riddles
loc_ques = {
    "A":[
        {"Guess the character:\n📓🖋💀":"Light Yagami"},
        {"Guess the character:\n💘🐍🗿":"Boa Hancock"},
        {"Guess the character:\n🧭🏴‍☠⚔🟢":"Zoro"},
        {"Guess the character:\n🔥👊📿":"Ace"},
        {"Guess the character:\n🤡🗡🏴‍☠":"Buggy"}
    ],
    "B":[
        {"Guess the character:\n👺🔥💀":"Madara"},
        {"Guess the character:\n😴⚡😭":"Zentisu"},
        {"Guess the character: [Copy and open the link in a new tab]\nhttps://drive.google.com/file/d/1vsgmHFR4eKgMYkJD1sf0ngCGjFb5x2QK/view?usp=drive_link":"Luffy"},
        {"Guess the character: [Copy and open the link in a new tab]\nhttps://drive.google.com/file/d/1MRw6uH4yhIMsEuxqtgn_YVU8cpN-Eu75/view?usp=drive_link":"White Beard"},
        {"Guess the character: [Copy and open the link in a new tab]\nhttps://drive.google.com/file/d/1zYHGyijLtQCuts2-_JqLQn3K-A4-3lJy/view?usp=drive_link":"Roger"}
    ],
    "C":[
        {"Guess the character: [Copy and open the link in a new tab]\nhttps://drive.google.com/file/d/1khi9JpNP2PABcK0OcnlxcyGuEfVoi8tz/view?usp=drive_link":"Black Beard"},
        {"Guess the character:\n❄👊🩸":"Akaza"},
        {"Guess the character:\n🐗👧🏻😤":"Inosuke"},
        {"Guess the character:\n🕵🏻👨‍👩‍👧💣":"Loid Forger"},
        {"Guess the character: [Copy and open the link in a new tab]\nhttps://drive.google.com/file/d/1-98rDwszU84w0OJuDOHDzBttRALUgf9u/view?usp=drive_link":"Sasuke Uchiha"}
    ],
    "D":[
        {"Guess the character: [Copy and open the link in a new tab]\nhttps://drive.google.com/file/d/1aarLn0Hck56-49ngh-Iz6PmBTQX-N_K3/view?usp=drive_link":"Eren Jaeger"},
        {"Guess the character: [Copy and open the link in a new tab]\nhttps://drive.google.com/file/d/1gsfkKDwA3mIujF58AsUNSdcsC3rmAOtt/view?usp=drive_link":"Itachi Uchiha"},
        {"Guess the character: [Copy and open the link in a new tab]\nhttps://drive.google.com/file/d/1VMMh1YvGwrijQvw4sk2YJn0UoHpC9XWC/view?usp=drive_link":"Sukuna"},
        {"Guess the character: [Copy and open the link in a new tab]\nhttps://drive.google.com/file/d/11eG6XBDhiv5WuKpXoX4uYHI64dbUTMdB/view?usp=drive_link":"Erwin"},
        {"Guess the character: [Copy and open the link in a new tab]\nhttps://drive.google.com/file/d/1tIScMqULJIktePlPj4Z2Xrnmwvv5M5AG/view?usp=drive_link":"Pain"}
    ]
}

loc_rid = {
    'A': [
        {"Let the books have a bite of snack": "1874"},
        {"Black soil is not a requirement for the cotton plant to grow!!!": "7022"},
        {"Take a seat; Next to the mechanical heat": "1245"},
        {"May the kids-play, lead you the way": "4910"},
        {"Where the new birds gather to feed;<br/>At the corner you'll find what you need.": "5378"}
    ],
    'B': [
        {"Look low in bronze, as the testament of peace lies at his feet.": "7504"},
        {"Where ideas and ventures soar, lies the clue yet to explore.": "3349"},
        {"Seek the lane near the place, where minds communicate with legal grace.": "3905"},
        {"Pay homage to the mother of our language.": "4873"},
        {"As the crocodiles stay still, the swans go for the kill.": "7553"}
    ],
    'C': [
        {"Savings, withdrawal, interest;<br/>Get to the union bush to have some rest.": "2206"},
        {"Our love for gitam lies lit;<br/>As the sparkling teeth once u get ur permit.": "8249"},
        {"Where thorns guard the treasure's trace;<br/>Unveil them alongside Gandhi's grace.": "2801"},
        {"Following the will of 'D', the parking lanes lead you to the mystical glee.": "2750"},
        {"When led by the infamous Shivaji, even the gardens bloom treasures.": "9655"}
    ],
    'D': [
        {"Where students from distant shores dwell, near the tree that once stood well.": "5252"},
        {"Near the fitness trails, in a quiet corner, the mystery prevails.": "6720"},
        {"Where cadets convene, in uniforms pristine and discipline is built within.": "7314"},
        {"In Coke Station's forgotten domain, where sweet corn was once the grain.": "7253"},
        {"Where tennis courts and cycles align, the open space where fitness defines.": "9180"}
    ]
}

def get_random_sector():
    sectors = ['A', 'B', 'C', 'D']
    return random.choice(sectors)

def get_random_riddle(sector):
    riddles = loc_rid[sector]
    return random.choice(riddles)

def get_random_question(sector):
    questions = loc_ques[sector]
    return random.choice(questions)

def validate_riddle(riddle, answer):
    correct_answer = list(riddle.values())[0]
    return str(answer) == str(correct_answer)

def validate_question(question, answer):
    correct_answer = list(question.values())[0]
    return answer.lower() == correct_answer.lower()

@app.route('/', methods=['GET'])
def start_game():
    session.clear()
    session['sectors_completed'] = []
    sector = get_random_sector()
    session['sector'] = sector
    session['score'] = 0
    riddle = get_random_riddle(sector)
    session['riddle'] = riddle
    return render_template('riddle.html', riddle_text=list(riddle.keys())[0])

@app.route('/check_riddle', methods=['POST'])
def check_riddle():
    answer = request.form['answer']
    riddle = session['riddle']
    if validate_riddle(riddle, answer):
        session['score'] += 1
        sector = session['sector']
        question = get_random_question(sector)
        session['question'] = question
        return render_template('question.html', question_text=list(question.keys())[0])
    else:
        return render_template('riddle.html', riddle_text=list(riddle.keys())[0], error='Incorrect answer, try again.')

@app.route('/check_question', methods=['POST'])
def check_question():
    answer = request.form['answer']
    question = session['question']
    if validate_question(question, answer):
        session['score'] += 1
        sectors = ['A', 'B', 'C', 'D']
        current_sector = session['sector']
        session['sectors_completed'].append(current_sector)
        if len(session['sectors_completed']) == len(sectors):
            return redirect(url_for('show_result'))
        next_sector_index = (sectors.index(current_sector) + 1) % len(sectors)
        next_sector = sectors[next_sector_index]
        session['sector'] = next_sector
        riddle = get_random_riddle(next_sector)
        session['riddle'] = riddle
        return render_template('riddle.html', riddle_text=list(riddle.keys())[0])
    else:
        return render_template('question.html', question_text=list(question.keys())[0], error='Incorrect answer, try again.')

@app.route('/result', methods=['GET'])
def show_result():
    score = session['score']
    if len(session['sectors_completed']) == 4:
        result_message = f'Congratulations! You completed all sectors. Your final score is {score}.'
    else:
        result_message = f'Game Over! You completed {len(session["sectors_completed"])} sectors. Your final score is {score}.'
    return render_template('result.html', result_message=result_message)

if __name__ == '__main__':
    app.run(debug=True)