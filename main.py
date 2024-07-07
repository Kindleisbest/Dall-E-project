from flask import Flask, render_template, request, send_from_directory, session
from openai import OpenAI
import os 
import requests
from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment

def create_assessment(
    project_id: str, recaptcha_key: str, token: str, recaptcha_action: str
) -> Assessment:
    """Create an assessment to analyze the risk of a UI action.
    Args:
        project_id: Your Google Cloud Project ID.
        recaptcha_key: The reCAPTCHA key associated with the site/app
        token: The generated token obtained from the client.
        recaptcha_action: Action name corresponding to the token.
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Set the properties of the event to be tracked.
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_key
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    project_name = f"projects/{project_id}"

    # Build the assessment request.
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    response = client.create_assessment(request)

    # Check if the token is valid.
    if not response.token_properties.valid:
        print(
            "The CreateAssessment call failed because the token was "
            + "invalid for the following reasons: "
            + str(response.token_properties.invalid_reason)
        )
        return

    # Check if the expected action was executed.
    if response.token_properties.action != recaptcha_action:
        print(
            "The action attribute in your reCAPTCHA tag does"
            + "not match the action you are expecting to score"
        )
        return
    else:
        # Get the risk score and the reason(s).
        # For more information on interpreting the assessment, see:
        # https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
        for reason in response.risk_analysis.reasons:
            print(reason)
        print(
            "The reCAPTCHA score for this token is: "
            + str(response.risk_analysis.score)
        )
        # Get the assessment name (id). Use this to annotate the assessment.
        assessment_name = client.parse_assessment_path(response.name).get("assessment")
        print(f"Assessment name: {assessment_name}")
    return response








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
