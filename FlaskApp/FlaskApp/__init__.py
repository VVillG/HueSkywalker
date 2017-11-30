from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")

def Main():
	return render_template("main.html")
if __name__ == "__main__":
	app.run("165.227.83.57")

