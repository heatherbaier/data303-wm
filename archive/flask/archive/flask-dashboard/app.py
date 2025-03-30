from flask import Flask, render_template # Import Flask

app = Flask(__name__) # Create a Flask instance

@app.route("/") # Define a route ("/") (kind of like a page basically) which loads index.html
def index():
    return render_template("index.html") # Render the index.html file

if __name__ == "__main__":
    app.run(debug=True) # debug=True helps us see errors while developing.