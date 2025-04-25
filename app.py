from flask import Flask, render_template_string, request
from catoligo_v1 import process_text  # Import the function from your script

app = Flask(__name__)

# HTML template for the user interface
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Catoligo App</title>
</head>
<body>
    <h1>Catoligo Text Processor</h1>
    <form method="POST">
        <textarea name="user_input" rows="5" cols="50" placeholder="Enter text here"></textarea><br>
        <input type="submit" value="Process">
    </form>
    {% if output %}
    <h2>Output:</h2>
    <pre>{{ output }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        output = process_text(user_input)  # Call the function from your script
    return render_template_string(html_template, output=output)

if __name__ == '__main__':
    app.run(debug=True)

def process_text(text):
    return text.upper()