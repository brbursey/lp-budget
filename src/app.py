from lp import LP
from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Greetings"


@app.route("/budget")
def budget():
    budget = {
        "income": (5000.00, 5000.00),
        "rent": (600.00, 600.00),
        "loans": (300.00, 700.00),
        "invest": (400.00, 600.00),
        "savings": (750.00, 1200.00),
        "groceries": (100.00, 400.00),
        "car": (200.00, 300.00),
        "tythe": (500.00, 500.00),
        "clothes": (50.00, 100.00),
        "gym": (30.00, 30.00),
        "emergency": (200.00, 400.00),
        "fun": (200.00, 300.00)
    }
    lp = LP(budget)
    results = lp.solve()
    stats = lp.get_stats(budget)
    return json.dumps(stats)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

# TODO: setup config for this to be deployed
# TODO: add code for discrete values (ex: subscriptions)
# TODO: Look into Quadratic Programming for more complex items like loans (quadprog)