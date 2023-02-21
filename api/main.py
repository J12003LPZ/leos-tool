import openai
from flask import Flask, request, render_template
from dotenv import load_dotenv
import os

# Load environment variables from .env file.
load_dotenv()

# Get the API key from the environment variable OPENAI_API_KEY.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__, template_folder="../templates",
            static_folder="../static")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set up Jinja2 template


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/grammar_check')
def about():
    return render_template('index.html')


# Summarize text using OpenAI GPT-3


@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.form["text"]
    length = request.form["summary-length"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"In {length} words rewrite in simple words the following text:\n\n{text}",
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    summary = response.choices[0].text.strip()

    # Check if summary is the same as the input text
    if summary == text:
        summary = "Unable to generate summary. Please enter a longer input text."

    return render_template("index.html", text=text, summary=summary)


# Start Flask app
if __name__ == "__main__":
    app.run(debug=True)
