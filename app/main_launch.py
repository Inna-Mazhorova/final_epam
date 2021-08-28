import configparser
from subprocess import PIPE, Popen, TimeoutExpired

from flask import Flask, json, render_template, request

app = Flask(__name__)


def get_injection(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


injection = get_injection("./config_directory/injection.txt")

config = configparser.ConfigParser()
config.read("./config_directory/config.ini")


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

    process = Popen(args, stdin=PIPE, stdout=PIPE,
                    stderr=PIPE, encoding=config['process']['encoding'])

    try:
        stdout, stderr = process.communicate(stdin, timeout=float(config['process']['timeout']))
    except TimeoutExpired:
        return json.dumps(
            {"output": "The program takes too long to execute",
             "error": str(config['process']['timeout'])
             }
        )

    return json.dumps({"output": str(stdout), "error": str(stderr)})


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8080)
