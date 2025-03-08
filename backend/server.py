from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import ollama
import numpy as np
from utils import generate_question_prompt, generate_summary_prompt

app = Flask(__name__)
CORS(app)

vector_store = []

def get_embedding(text):
    """
    Placeholder embedding function.
    Replace this with a proper embedding model, for example:
      model = SentenceTransformer('all-MiniLM-L6-v2')
      return model.encode(text)
    """
    # For demonstration, we create a simple normalized vector based on character ordinals.
    vec = np.array([float(sum(bytearray(text, 'utf-8')) % (i+1)) for i in range(300)])
    norm = np.linalg.norm(vec) or 1.0
    return vec / norm

def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / ((np.linalg.norm(vec1) * np.linalg.norm(vec2)) or 1.0)

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get('text') if data else None
    if not text:
        return jsonify({"message": "No text received"}), 400

    # Check if we already have an embedding for this text.
    # For simplicity we compare exact text.
    existing = next((entry for entry in vector_store if entry["text"] == text), None)
    if not existing:
        print("Creating embedding for new text...")
        embedding = get_embedding(text)
        vector_store.append({"text": text, "embedding": embedding})
    else:
        print("Embedding already exists for this text.")

    try:
        def generate():
            print("\n" + "-"*50 + "\nSummary Generation Started.")
            for chunk in ollama.generate(
                model='llama3.2', 
                prompt=generate_summary_prompt(text=text[:4000]),
                stream=True
            ):
                # Extract only the 'response' field.
                response_text = chunk.get('response', '')
                yield f"data: {response_text}\n\n"
            yield "data: [DONE]\n\n"
        print("Summary Generation Done!")
        return Response(generate(), mimetype='text/event-stream')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/question', methods=['POST'])
def solve_question():
    data = request.get_json()
    # Instead of using the provided "text" we retrieve it from our vector store.
    question = data.get('question') if data else None
    if not question:
        return jsonify({"message": "Question is required"}), 400

    if not vector_store:
        return jsonify({"message": "No text has been processed yet"}), 400

    # For a RAG style approach, we compute the question embedding and then retrieve
    # the stored text with the highest cosine similarity.
    question_embedding = get_embedding(question)
    best_match = None
    best_score = -1
    for entry in vector_store:
        score = cosine_similarity(question_embedding, entry["embedding"])
        if score > best_score:
            best_score = score
            best_match = entry["text"]

    # Now, use the best matching text as context for answering the question.
    # Adjust generate_question_prompt to accept context if needed.
    try:
        def generate():
            print("Generating answer using retrieved context.")
            for chunk in ollama.generate(
                model='llama3.2', 
                prompt=generate_question_prompt(text=best_match, question=question),
                stream=True
            ):
                response_text = chunk.get('response', '')
                yield f"data: {response_text}\n\n"
            yield "data: [DONE]\n\n"
        return Response(generate(), mimetype='text/event-stream')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
