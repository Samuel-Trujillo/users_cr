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

    user_id= mysql.query_db(query, data)
    return redirect(f"/individual/{user_id}")

@app.route('/create')
def add_form():
    return render_template('create.html')

@app.route("/indi_math/<int:user_id>")
def individual (user_id):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        'id' : user_id
    }
    result =connectToMySQL('users_schema').query_db(query, data)
    return redirect('/')

@app.route('/individual/<int:user_id>')
def individual_show(user_id):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        'id' : user_id
    }
    result =connectToMySQL('users_schema').query_db(query, data)
    return render_template('individual.html', user = result[0])

@app.route('/edit/<int:user_id>')
def edit_show(user_id):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        'id' : user_id
    }
    result =connectToMySQL('users_schema').query_db(query, data)
    print(result[0])
    return render_template('edit.html', user = result[0])

@app.route("/edit_math/<int:user_id>", methods=["POST"])
def edit(user_id):
    query= "UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s, updated_at = NOW() WHERE id = %(id)s;"
    data = {
        'id' : user_id,
        'fn': request.form['first'],
        'ln': request.form['last'],
        'em': request.form['email']
    }
    result = connectToMySQL('users_schema').query_db(query, data)
    return redirect("/")

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    query = "DELETE FROM users WHERE id = %(id)s;"
    data = {
        'id' : user_id
    }
    result =connectToMySQL('users_schema').query_db(query, data)
    return redirect('/')



            
if __name__ == "__main__":
    app.run(debug=True)