import eel
import os

# Initialize Eel
dirname = os.path.dirname(__file__)
eel.init(dirname)


# Define a Python function that can be called from JavaScript
@eel.expose
def get_message():
    return "Hello from Python!"


# Start the Eel application with custom host and port
eel.start("index.html", size=(300, 200), host="localhost", port=8080)
