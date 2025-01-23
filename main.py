from flask import Flask, render_template, request, send_from_directory, session, redirect
from openai import OpenAI
import os 
import requests
from replit import db #For login
import logging #For login
from werkzeug.security import generate_password_hash, check_password_hash #For login

logging.basicConfig(level=logging.DEBUG)

 
app = Flask(__name__) # sets up the app routes
client = OpenAI(api_key= "Change this to an actual key") #Sets the API key
api_key = os.getenv('OPENAI_API_KEY') #Uses the API key sevice so we can equal it to a key
app.secret_key = "nonsense"
db = {}



@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, "static"), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
  
  return render_template("home.html")#Change to index.html
  #creates the home page

# @app.route('/loggingin', methods=["POST", "GET"])
# def loggin():
#   if request.method == "POST":
#     Username = request.form["Username"]
#     Password = request.form["Password"]
#     Signup = request.form["Signup"]

#     session['Signup'] = Signups
#     session["Username"] = Username
#     session["Password"] = Password
    
#     if Username in db:
#       if Password == db[Username]:
#         return render_template("home.html")
#       else:
#         return "Incorrect Password"
#     else:
#       return "Incorrect Username"

#   return render_template("index.html")
  
#     # db[Username] = username_text
  

# @app.route('/signup', methods=["POST", "GET"])
# def signups():
#     if request.method == "POST":
#       logging.debug(f"Received data: {request.form}")
#       username = request.form.get("Username")
#       password = request.form.get("Password")
#       admin_password = request.form.get("AdminPassword")
#       signup = request.form.get("Signup")

      # Store session data
      # session['Signup'] = signup
      # session["Username"] = username

      # Define your admin password (this should ideally be stored securely)
     # correct_admin_password = "Ridge_Rules"  # Replace with your actual admin password

    #  if signup != "Signup":
     #   return render_template("signup.html")  # Handle unexpected signup values

    #   if username in db:
    #     return render_template("signup.html", error="User already exists"), 400

    #   if not password or password.strip() == "":
    #     return render_template("signup.html", error="Password is required"), 400

    #   if admin_password != correct_admin_password:
    #     return render_template("signup.html", error="Invalid admin password"), 403

    #   hashed_password = generate_password_hash(password)
    #   db[username] = hashed_password
    #   return redirect("/")  # Redirect to a home page after signup

    # return render_template("home.html")  # Handle GET request to show signup form


@app.route('/homepage')
def login():
  session["picture"] = ""
  return render_template("home.html")
  #creates the home page

@app.route("/index", methods=["POST", "GET"])
def reset():
  #request.form["index"]
    response = client.images.generate(
    model="dall-e-3",
    prompt=session["picture"],
    size="1024x1024",
    quality="standard",
    n=1,)# it takes the prompt and the image model dalle and generate an image through dalle and displays it on the website

    print(response.data[0].url)
    return render_template("generateImage.html", response=response)

@app.route("/home", methods=["POST", "GET"])
def home():
  return render_template("index.html")


@app.route('/generateImage', methods=["POST", "GET"])
def makeImage():
    if request.method == "POST":
        prompt = request.form["imagePrompt"]
        session["picture"] = prompt
        prompt_text = f"Generate an image based on the prompt: {prompt}"
    response = client.images.generate(
      model="dall-e-3",
      prompt=request.form["imagePrompt"],
      size="1024x1024",
      quality="standard",
      n=1,
    )# it takes the prompt and the image model dalle and generate an image through dalle and displays it on the website

    print(response.data[0].url)
    return render_template("generateImage.html", response=response) # It passes the variabes for in to be used as jinja in the html to display the image




if __name__ == '__main__':
    app.run(host ='0.0.0.0', port=3001, debug=True) # makes the website run
