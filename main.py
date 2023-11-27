from flask import Flask, render_template, request, redirect, url_for, session
import pickle

app = Flask(__name__)
app.secret_key = '187jhhf'  # Change this to a secure secret key

pipe = pickle.load(open("email.pkl", "rb"))

# User registration data
users = []


@app.route('/', methods=["GET", "POST"])
def main_function():
    if request.method == "POST":
        text = request.form
        emails = text['email']
        list_email = [emails]
        output = pipe.predict(list_email)[0]
        return render_template("show.html", prediction=output)
    elif 'username' in session:
        return render_template("index.html")
    else:
        return render_template('signup.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Check if the username is already taken
        if any(user['username'] == username for user in users):
            return "Username already taken. <a href='/signup'>Try again</a>"
        # Store the user registration data 
        users.append({'username': username, 'password': password})
        return render_template("signin.html")
    return render_template("signup.html")

@app.route('/signin', methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Check if the provided username and password match any registered user
        if any(user['username'] == username and user['password'] == password for user in users):
            session['username'] = username  # Store the username in a session
            return "Signin successful. Welcome, {}! <a href='/'>Go to main page</a>".format(username)
        return "Signin failed. <a href='/signin'>Try again</a>"
    return render_template("signin.html")

if __name__ == '__main__':
    app.run(debug=True)