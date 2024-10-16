from flask import Flask, render_template, request, send_from_directory, session
from openai import OpenAI
import os 
import requests
from replit import db

 
app = Flask(__name__) # sets up the app routes
client = OpenAI(api_key= "Change this to an actual key") #Sets the API key
api_key = os.getenv('OPENAI_API_KEY') #Uses the API key sevice so we can equal it to a key
app.secret_key = "nonsense"



@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, "static"), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
  
  return render_template("index.html")#creates the home page

@app.route('/loggingin', methods=["POST", "GET"])
def loggin():
  session["Username"] = ""
  if request.method == "POST":
    Username = request.form["Username"]
    session["Username"] = Username
    if Username in db:
      session["Password"] = ""
      if request.method == "POST":
        Password = request.form["Password"]
        session["Password"] = Password
        if Password in db:
          return render_template("home.html")
        else:
          return("Incorrect Password")
    else:
      return("Incorrect Username")
  
    # db[Username] = username_text
  

@app.route('/signup', methods=["POST", "GET"])
def signups():

  return render_template("signup.html")

@app.route('/homepage')
def login():
  session["picture"] = ""
  return render_template("home.html")#creates the home page

@app.route("/index", methods=["POST", "GET"])
def reset():
  #request.form["index"]
    response = client.images.generate(
    model="dall-e-3",
    prompt=session["picture"],
    size="1024x1024",
    quality="standard",
    n=1,
  )# it takes the prompt and the image model dalle and generate an image through dalle and displays it on the website

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
