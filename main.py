from flask import Flask, render_template, request, send_from_directory, session
from openai import OpenAI
import os 
import requests

my_secret = os.environ['Key'] 
app = Flask(__name__) # sets up the app routes
client = OpenAI(api_key= "sk-proj-a5wdJlvsikdxaXuppqSzT3BlbkFJPNwDmZ2xr0pJ0rsb2SLe") #Sets the API key
api_key = os.getenv('OPENAI_API_KEY') #Uses the API key sevice so we can equal it to a key
app.secret_key = "nonsense"



@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, "static"), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
  session["picture"] = ""
  return render_template("index.html")#creates the home page

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
    app.run(host ='0.0.0.0', port=81, debug=True) # makes the website run
