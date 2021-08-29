import configparser
import os
from subprocess import PIPE, Popen, TimeoutExpired

from flask import Flask, json, render_template, request

app = Flask(__name__)


def get_injection(name) -> str:
    with open(os.path.join(path, f"./config_directory/{name}"), "r") as file:
        return file.read()


path = os.path.dirname(os.path.abspath(__file__))


config = configparser.ConfigParser()
config.read(os.path.join(path, "./config_directory/config.ini"))
injection = get_injection(config["server"]["injection"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/compile", methods=["POST"])
def compile() -> str:
    content = request.get_json()
    code = injection + "\n" + content["input_code"]
    stdin = content["input_stdin"]
    args = [
        "python",
        "-c",
        code,
        config["blocked"]["imports"],
        config["blocked"]["functions"],
    ]

    process = Popen(
        args,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        encoding=config["process"]["encoding"],
    )

    try:
        stdout, stderr = process.communicate(
            stdin, timeout=float(config["process"]["timeout"])
        )
    except TimeoutExpired:
        return json.dumps(
            {
                "output": "The program takes too long to execute",
                "error": str(config["process"]["timeout"]),
            }
        )

    return json.dumps({"output": str(stdout), "error": str(stderr)})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
