from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from langchain.schema import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.llms import Ollama
import re

def fix_broken_words(text):
    # This regex finds patterns where a letter or punctuation is followed by a space and then another letter.
    # It removes the space, joining them into one word.
    fixed_text = re.sub(r'(?<=\w)\s+(?=\w)', '', text)
    return fixed_text

app = Flask(__name__)
CORS(app)

# ------------ Initialize Core Variables ------------
vector = None
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
embeddings = OllamaEmbeddings(model="llama3.2")
model = Ollama(model="llama3.2")

# Define prompt template for question answering
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context and check for grammatical correctness and DONT GIVE ANY BROKEN WORDS:

<context>
{context}
</context>

Question: {input}""")

retriever = None
retrieval_chain = None

def update_vector_store(text):
    """
    Create or update the vector store from the provided text.
    """
    global vector, retriever, retrieval_chain
    docs = [Document(page_content=text)]
    documents = text_splitter.split_documents(docs)
    if vector is None:
        vector = FAISS.from_documents(documents, embeddings)
    else:
        vector.add_documents(documents)
    retriever = vector.as_retriever()
    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

@app.route('/generate_embedding', methods=['POST'])
def generate_embedding():
    data = request.get_json()
    text = data.get('text') if data else None
    if not text:
        return jsonify({"message": "No text provided"}), 400
    update_vector_store(text)
    return jsonify({"message": "Vector embedding generated successfully."})

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get('text') if data else None

    if not text:
        return jsonify({"message": "No text received"}), 400

    # Update the vector store using the provided text
    update_vector_store(text)

    try:
        def generate():
            print("\n" + "-" * 50 + "\nSummary Generation Started.")
            buffer = ""
            
            for chunk in model.stream(f"Summarize the following content: {text[:4000]}"):
                response_text = chunk  # chunk is expected to be a string
                buffer += chunk

                if buffer and buffer[-1] in " .,\n":
                    # Fix broken words in the current buffer
                    response_text = fix_broken_words(buffer)
                    # print(response_text, end="", flush=True)
                    buffer = ""
                yield f"data: {response_text}\n\n"
            if buffer:
                    response_text = fix_broken_words(buffer)
                    # print(response_text, end="", flush=True)
            yield f"data: {response_text}\n\n"
            yield "data: [DONE]\n\n"

        print("Summary Generation Done!")
        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/question', methods=['POST'])
def solve_question():
    data = request.get_json()
    question = data.get('question') if data else None
    # If text is provided with the question, update the vector store.
    text = data.get('text') if data else None

    print("Question asked -", question)
    if not question:
        return jsonify({"message": "Question is required"}), 400

    if text:
        update_vector_store(text)
    elif vector is None:
        return jsonify({"message": "No text provided and vector store is empty. Please provide text."}), 400

    if retriever is None or retrieval_chain is None:
        return jsonify({"message": "The vector store or retrieval chain is not ready. Please provide text first."}), 400

    try:
        # Invoke the retrieval chain with the question
        response_stream = retrieval_chain.stream({"input": question})
        def generate():
            print("Generating answer using retrieved context.")
            for chunk in response_stream:
                if "answer" in chunk:
                    yield f"data: {chunk['answer']}\n\n"
            yield "data: [DONE]\n\n"
        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
