from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
from utils import generate_question_prompt, generate_summary_prompt
import time

app = Flask(__name__)
CORS(app)
@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = None
    if data:
        if 'text' in data:
            text = data['text']
    if not text:
        return jsonify({"message": "No text received"}), 400
    
    try:
        response = ollama.generate(model='llama3.2', prompt=generate_summary_prompt(text=text[:4000]))
        summary = response['response']
        # summary = "The is a demo summary of the text"
        print("\n\n",("-"*50))
        print("Summary generated \n",summary)
        
        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/question',methods=['POST'])
def solve_question():
    data = request.get_json()
    text = None
    question = None
    if data:
        if 'text' in data:
            text = data['text']
        if 'question' in data:
            question = data['question']
        
    try:
        print("\n\n",("-"*50))
        print("Question Asked \n",question)
        response = ollama.generate(model='llama3.2', prompt=generate_question_prompt(text=text,question=question))
        ans = response['response']
        print("\n\n",("-"*50))
        print("Summary generated \n",ans)
        
        return jsonify({"answer":ans}), 200
    except Exception as e:
        return jsonify({"error",str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)
