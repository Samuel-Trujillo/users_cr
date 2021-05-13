from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('users_schema')	        # call the function, passing in the name of our db
    users = mysql.query_db('SELECT * FROM users;')  # call the query_db function, pass in the query as a string
    return render_template("read_all.html", all_users = users)

@app.route("/create_math", methods=["POST"])
def add_user ():
    mysql = connectToMySQL('users_schema')
    query = "INSERT INTO users(first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, NOW(), NOW());" 
    data = {
        'fn': request.form['first'],
        'ln': request.form['last'],
        'em': request.form['email']
    }

    mysql.query_db(query, data)
    return redirect("/")

@app.route('/create')
def add_form():
    return render_template('create.html')

            
if __name__ == "__main__":
    app.run(debug=True)