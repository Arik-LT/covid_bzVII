from covid import app

@app.route("/")
def index():
    return "Funciona desde views"