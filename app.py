from flask import Flask, render_template, request, jsonify
from plot import buf_remaining, plot

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


##
## {"code":"PA90,90;PD;PA90,900;PA900,900;PA900,90;PA90,90;"}

@app.route("/plot", methods=["POST"])
def handle_plot():
    print(request.get_json())
    data = request.get_json()

    code: str = data.get("code")
    commands = code.strip().split(';')

    plot(commands)

    return jsonify({"buf_remaining": buf_remaining(), "status": "success", "message": "Plotting command received.", "code ": code}), 200

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
