import os
from chatbot import app  # Import the Flask app from chatbot.py

# Set up the WSGI application callable
if __name__ == "__main__":
    app.run()

# WSGI application
application = app
