from flask import Flask, request, jsonify

import catoligo_v1  # Assuming catoligo_v1.py contains the logic you want to use

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    try:
        # Get input data from the request
        input_data = request.json
        if not input_data:
            return jsonify({"error": "No input data provided"}), 400

        # Call the function from catoligo_v1 with the input data
        result = catoligo_v1.process_data(input_data)  # Replace 'process_data' with the actual function name

        # Return the result as JSON
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the CatOligo API!", 200

if __name__ == '__main__':
    app.run(debug=True)