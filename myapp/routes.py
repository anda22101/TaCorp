from myapp import create_app

app = create_app()


@app.route("/")
def index():
 return "Welcome to the Flask App!"
