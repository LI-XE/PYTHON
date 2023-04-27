from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, we did it!"


@app.route("/home/<string:name>/<int:num>")
def home(name, num):
    return render_template("index.html", name=name, num=num)


@app.route("/number/<num>")
def number(num):
    return num


if __name__ == "__main__":
    app.run(debug=True, port=5001)
