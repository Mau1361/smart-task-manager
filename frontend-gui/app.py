from flask import Flask, render_template, request, redirect, session
import requests
import os
app = Flask(__name__)
app.secret_key = 'supersecret'

AUTH_URL = os.environ.get("AUTH_URL", "http://localhost:5000")
TASK_URL = os.environ.get("TASK_URL", "http://localhost:5001")


@app.route('/')
def home():
    if 'token' not in session:
        return redirect('/login')

    try:
        resp = requests.get(f"{TASK_URL}/tasks")
        tasks = resp.json()
    except:
        tasks = []
    return render_template('dashboard.html', tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            "email": request.form['email'],
            "password": request.form['password']
        }
        resp = requests.post(f"{AUTH_URL}/login", json=data)
        if resp.status_code == 200:
            session['token'] = resp.json().get('token')
            return redirect('/')
        else:
            return "<h3>Login failed</h3>", 401
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }
        try:
            response = requests.post(f"{AUTH_URL}/signup", json=data)
            if response.status_code == 201:
                return redirect('/login')
            else:
                return f"<h3>Signup failed: {response.status_code} - {response.text}</h3>", 400
        except Exception as e:
            return f"<h3>Exception: {str(e)}</h3>", 500
    return render_template("signup.html")

@app.route('/add-task', methods=['POST'])
def add_task():
    if 'token' not in session:
        return redirect('/login')

    data = {
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "status": request.form.get("status", "pending")
    }

    try:
        resp = requests.post(f"{TASK_URL}/task", json=data)
        return redirect('/')
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>"

@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 'token' not in session:
        return redirect('/login')

    try:
        requests.delete(f"{TASK_URL}/task/{task_id}")
        return redirect('/')
    except Exception as e:
        return f"<h3>Error deleting task: {str(e)}</h3>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
