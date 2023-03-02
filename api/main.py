import openai
from flask import Flask, request, render_template
import docx2txt

# Initialize Flask app
app = Flask(__name__, template_folder="../templates",
            static_folder="../static")

# Set OpenAI API key
openai.api_key = "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"

# Set up Jinja2 template
@app.route("/")
def index():
    return render_template("grammar_checker.html")


@app.route('/<string:page_name>')
def render_template_page(page_name):
    return render_template(f"{page_name}.html")


# Flask routes
@app.route("/translate_text", methods=["POST"])
def translate():
    text = request.form["text"]
    language = request.form["language"]
    response = openai.Completion.create(
        engine="text-curie-001",
        prompt=f"Translate the following text in {language}:\n\n{text}",
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    translated_text = response.choices[0].text.strip()

    return render_template("translator.html", text=text, translated_text=translated_text)

    
# Summarize text using OpenAI GPT-3
@app.route("/summarize", methods=["POST"])
def summarize():
    if 'my_file' in request.files:
        file = request.files['my_file']
        filename = file.filename
        if filename != '':
            # Check if file is a word document
            if filename.endswith('.docx'):
                text = docx2txt.process(file)
        else:
            text = ''

        if text != '':
            length = request.form["summary-length"]
            response = openai.Completion.create(
                engine="text-davinci-002",
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

            return render_template("summarizer.html", text=text, summary=summary)

    # If no file was uploaded or if the file is empty, summarize the text provided in the text input field
    text = request.form["text"]
    if text != '':
        length = request.form["summary-length"]
        response = openai.Completion.create(
            engine="text-davinci-002",
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

        return render_template("summarizer.html", text=text, summary=summary)

    # If no file was uploaded and no text was provided, show an error message
    return render_template("error.html", message="Please upload a file or enter some text.")

# Generate text using OpenAI GPT-3
@app.route("/grammar_checker", methods=["POST"])
def grammar():
    text = request.form["text"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Correct the misspellings in the following text:\n\n{text}",
        max_tokens=1024,
        temperature=0.1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    fixed_text = response.choices[0].text.strip()

    # Check if summary is the same as the input text
    if  fixed_text == text:
         fixed_text = "Unable to generate summary. Please enter a longer input text."

    return render_template("grammar.html", text=text,  fixed_text=fixed_text)


# Generate text using OpenAI GPT-3
@app.route("/paraphraser_text", methods=["POST"])
def paraphraser():
    text = request.form["text"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Paraphrase the following text:\n\n{text}",
        max_tokens=1024,
        temperature=0.8,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    paraphraser = response.choices[0].text.strip()

    # Check if summary is the same as the input text
    if  paraphraser == text:
         paraphraser = "Unable to generate summary. Please enter a longer input text."

    return render_template("paraphraser.html", text=text,  paraphraser=paraphraser)

# Generate text using OpenAI GPT-3
@app.route("/plagiarism_text", methods=["POST"])
def plagiarism_checker():
    text = request.form["text"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"You are going to verify and if the following text is plagiarized and you are going to give me a percentage of what you think is plagiarized:\n\n{text}\n\nhighlight the sentences that are from another source",
        max_tokens=1024,
        temperature=0.8,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    plagiarism_opinion = response.choices[0].text.strip()

    # Check if summary is the same as the input text
    if  plagiarism_opinion == text:
         plagiarism_opinion = "Unable to generate summary. Please enter a longer input text."

    return render_template("plagiarism_checker.html", text=text,  plagiarism_opinion=plagiarism_opinion)


# Start Flask app
if __name__ == "__main__":
    app.run(debug=True)
