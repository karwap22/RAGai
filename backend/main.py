# text = '''[Sarvam.ai] speech_team - Hiring Challenge'25 Submission
# This form collects submission to the tasks outlined in the Hiring challenge's Colab Notebook and some general information.



# We're Excited to Offer the Following Opportunities (Full Time only):

# 🌱 Summer Internship (2 months on-site/remote, earning up to 50k per month): Perfect for the enthusiastic learner! If you're a fresher or currently pursuing your undergraduate or postgraduate studies and have a foundational grasp of ML and programming, this internship is your stepping stone. You’ll gain hands-on experience and build practical knowledge while assisting with cutting-edge projects in the speech domain.

# Data Engineer: Dive into the world of web scraping, manage distributed data processing, and craft robust data pipelines.
# ML Engineer: Get your hands on training state-of-the-art (SOTA) speech models on powerful GPU clusters. Make an impact by pushing the boundaries of what our AI can learn!

# 🔥 AI Residency (6 months on-site, earning up to 1L per month): Designed for those with a solid foundation and ready to level up! This program is for individuals who have some professional experience or have demonstrated significant expertise in their domain. Here, you'll not only refine your skills but also actively contribute to our groundbreaking projects.

# Data Engineer: Tackle large-scale data mining and take charge of sophisticated engineering tasks. You'll develop and optimize extensive data pipelines tailored for massive data flows in the speech domain.
# ML Engineer: Embrace the challenge of training advanced speech models. Utilize top-tier deep learning frameworks like PyTorch and JAX, and explore powerful libraries such as NeMo and HuggingFace Transformers. Push technological limits and drive innovation within our team.
# paawankarwa22@gmail.com Switch accounts
 
# The name, email address and photo associated with your Google Account will be recorded when you upload files and submit this form
# * Indicates required question
# Name

# *
# Your answer
# Email Address
# *
# Your answer
# Phone Number (optional)
# Your answer
# Link to the completed Colab Notebook


# Make sure its shareable with viewing access to abhigyan@sarvam.ai

# *
# Your answer
# Applying for
# *
# Summer Internship (2 months full-time)
# AI Residency (6 months full-time)
# Role Preference
# *
# Data Engineer
# ML Engineer
# Preferred Location
# *
# Bengaluru
# Chennai
# Remote
# When are you available from?
# *
# DD
# /
# MM
# /
# YYYY
# Upload your latest Resume
# *
# Upload 1 supported file. Max 10 MB.
# Add File
# Github Link to your most exciting Project
# *
# Your answer
# Submit
# Clear form
# Never submit passwords through Google Forms.
# This form was created inside sarvam.

# Does this form look suspicious? Report

#  Forms
 
# Help and feedback'''

# from langchain.schema import Document
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import create_retrieval_chain
# from langchain_community.llms import Ollama

# # Suppose you have a variable 'text' that contains your source text.
# docs = [Document(page_content=text)]

# # Split the text into chunks to form documents.
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# documents = text_splitter.split_documents(docs)

# # Create embeddings and a vector store.
# embeddings = OllamaEmbeddings(model="llama3.2")
# vector = FAISS.from_documents(documents, embeddings)
# retriever = vector.as_retriever()

# # Initialize your LLM and prompt.
# model = Ollama(model="llama3.2")
# prompt = ChatPromptTemplate.from_template(
#     """Answer the following question based only on the provided context:

# <context>
# {context}
# </context>

# Question: {input}"""
# )

# # Create the document chain and the retrieval chain.
# document_chain = create_stuff_documents_chain(model, prompt)
# retrieval_chain = create_retrieval_chain(retriever, document_chain)

# # Instead of streaming, call the chain normally to get the full result including source documents.
# result = retrieval_chain.invoke({"input": "What was the name of the company that posted it?"})

# print("-------Context-------")
# cnt = 1
# # Print the final answer.
# if "context" in result:
#     for i in result["context"]:
#         print("NO - ",cnt)
#         print(i.page_content)
#         cnt +=1
# print("\n"*5)

# # Print the context that was used (i.e. the source documents).
# print("\nContext Used:")
# for doc in result.get("source_documents", []):
#     print(doc.page_content)





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
                print(response_text)
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
