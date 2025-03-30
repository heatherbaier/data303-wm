from flask import Flask, render_template     
app = Flask(__name__)   # Flask constructor 
  
# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')       
def hello(): 
    var = "Heather"
    return render_template("index.html", name = var)
  
if __name__=='__main__': 
   app.run(debug = True) 
