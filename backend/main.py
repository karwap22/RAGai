# import PyPDF2
# import ollama
# import re

# def extract_text_from_pdf(file_path):
#     # Create a PDF reader object
#     pdf_reader = PyPDF2.PdfReader(file_path)
    
#     # Extract text from the PDF file
#     text = ''
#     for page in range(len(pdf_reader.pages)):
#         text += pdf_reader.pages[page].extract_text() or ''
        
#     return text.strip()

# def preprocess_text(text):
#     # Remove punctuation, convert to lowercase, and tokenize the text
#     text = re.sub(r'[^\w\s]', '', text)
#     text = text.lower()
#     tokens = text.split()
    
#     return tokens

# def generate_response(pdf_text, user_question):
#     # Generate a response using Ollama's chat API based on the PDF text and user question
#     context = f"Context: {pdf_text}\n\nQuestion: {user_question}"
#     response = ""
#     for chunk in ollama.chat(model="llama3.2", messages=[{"role": "user", "content": context}], stream=True):
#         response += chunk["message"]["content"]
#         print(chunk["message"]["content"],end="")
    
#     return response

# def main():
#     file_path = "/Users/paawankarwa/Desktop/projects/pdfRAG/SDE_Resume_Single.pdf"
#     text = extract_text_from_pdf(file_path)
#     while True:
#         user_question = input("Enter your question: ")
#         print("--->",end="")
#         response = generate_response(text, user_question)
#         print()

# if __name__ == "__main__":
#     main()




from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased")
text = "The sun rises in the east. Plants perform photosynthesis. Water boils at 100 degrees Celsius. The earth orbits the sun in 365 days."
question = "What is the process by which plants make food?"


result = qa_pipeline({
    'context': text,
    'question': question
})

print(f"Answer: {result['answer']}")
print(f"Start position: {result['start']}")
print(f"End position: {result['end']}")
