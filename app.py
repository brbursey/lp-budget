from lp import LP

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
lp.get_stats(budget)

# TODO: setup config for this to be deployed
# TODO: add code for discrete values (ex: subscriptions)
# TODO: Look into Quadratic Programming for more complex items like loans (quadprog)