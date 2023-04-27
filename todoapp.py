from flask import Flask, render_template, request, redirect, url_for
import re
import pickle
import os

app = Flask(__name__, template_folder='templates')
if os.path.exists('todo_list.pkl'):
    with open('todo_list.pkl', 'rb') as f:
        todo_list = pickle.load(f)
else:
    todo_list = []

@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('index.html', todo_list=todo_list)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return redirect(url_for('index', error='Invalid email address'))
    
    valid_priorities = ['Low', 'Medium', 'High']
    if priority not in valid_priorities:
        return redirect(url_for('index', error='Invalid priority'))
    new_task = f'{task} ({email}) - {priority} priority'
    todo_list.append(new_task)
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    todo_list.clear()
    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save():
    with open('todo_list.pkl', 'wb') as f:
        pickle.dump(todo_list, f)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()