from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({"message": "No text received"}), 400
    try:
        response = ollama.generate(model='llama3.2', prompt=f"Summarize the following text:\n{text[:4000]}")
        print(response)
        summary = response['response']
        # summary = "The is a demo summary of the text"

        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)
