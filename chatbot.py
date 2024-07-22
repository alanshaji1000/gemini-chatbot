"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

from flask import Flask, render_template, request
import os
import google.generativeai as genai
from dotenv import load_dotenv
from markupsafe import Markup

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define generation config
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

history = []

@app.route("/")
def home():
    return render_template("index.html", history=history)  # Pass history to template

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"]

    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(user_input)
    model_response = response.text.replace('\n', '<br>')  # Replace newlines with HTML line breaks

    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [Markup(model_response)]})

    return render_template("index.html", history=history)

if __name__ == "__main__":
    app.run(debug=True)
