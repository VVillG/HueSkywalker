from flask import Flask, render_template, flash, url_for, redirect, request, session, make_response
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
from db_connect import connection


app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def Main():
	return render_template("main.html")

@app.route("/dashboard/", methods = ["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/portfolio/", methods = ["GET", "POST"])
def portfolio():
    return render_template("portfolio.html")

@app.route("/contact/", methods = ["GET", "POST"])
def contact():
    return render_template("contact.html")

@app.route("/about/", methods = ["GET", "POST"])
def about():
    return render_template("about.html")

@app.route("/summerResearch/", methods = ["GET", "POST"])
def summerResearch():
    return render_template("summerResearch.html")

@app.route("/AMIC/", methods = ["GET", "POST"])
def AMIC():
    return render_template("AMIC.html")
    
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice', [validators.Required()])

@app.route("/login/", methods = ["GET", "POST"])
def login():
    error = ""
    try:
        c, conn = connection()
        if request.method == "POST":
            data = c.execute("SELECT * FROM users WHERE username = ('{0}')".format(thwart(request.form['username'])))
            
            data = c.fetchone()[2]
            
            if sha256_crypt.verify(request.form['password'],data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                
                flash("You are now logged in!")
                return redirect(url_for("dashboard"))
        
            else:
                error = "Invalid Credentials. Please Try Again. 1"
                
            gc.collect()

        return render_template("login.html", error = error)

    except Exception as e:
        flash(e) 
        error = "Invalid Credentials. Please Try Again. 2"
        return render_template("login.html", error = error)
    
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = ('{0}')".format((thwart(username))))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('Register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES ('{0}','{1}','{2}','{3}')".format(thwart(username), thwart(password), thwart(email), thwart("/dashboard/")))

                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("Register.html", form=form)

    except Exception as e:
        return(str(e))
    
@app.route('/sitemap.xml/', methods=['GET'])
def sitemap():
    try:
        pages = []
        week = (datetime.now() - timedelta(days = 7)).date().isoformat()
        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods and len(rule.arguments)==0:
                pages.append(
                    ["http://165.227.83.57"+str(rule.rule),week]
                )
        sitemap_xml = render_template('sitemap_template.xml', pages = pages)
        response = make_response(sitemap_xml)
        response.headers["Content-Type"] = "application/xml"
        return response
    except Exception as e:
        return(str(e))

@app.route('/robots.txt/')
def robots():
    #return("User-agent: *\nDisallow /") #Disallows all robot traffic
    return("User-agent: *\nDisallow: /register/\nDisallow: /login/") #Disallows robot traffic to sensitive urls    

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("405.html")

@app.errorhandler(500)
def int_server_error(e):
    return render_template("500.html", error = e)

if __name__ == "__main__":
	app.run("165.227.83.57")

