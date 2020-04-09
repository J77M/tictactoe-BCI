from flask import Flask, render_template, request, session, redirect, url_for
# from flask_session import Session

app = Flask(__name__)
# PROPERTIES --->

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.debug = True
# <---

# Session(app)


@app.route("/")
def index():
    # check connection - if not connected render : connect else dashboard
    return render_template("connect.html")



if __name__ == "__main__":
    app.run()