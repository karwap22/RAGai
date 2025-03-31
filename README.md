
# Demo

https://github.com/user-attachments/assets/afcd5b70-7237-4057-9bce-ef7c352944ed

# AI Buddy Extension

A browser extension that extracts text from webpages, generates summaries, and answers questions using Retrieval-Augmented Generation (RAG) with Ollama.

![AI Buddy Extension](frontend/icon.png)

## Features

- **Text Extraction**: Extracts all text content from the current webpage
- **AI-Powered Summarization**: Generates concise summaries of webpage content using Ollama LLM
- **RAG-Based Q&A**: Ask questions about the webpage content and get contextually relevant answers
- **Persistent Storage**: Summaries and answers are saved per URL for quick reference
- **Real-Time Streaming**: View summaries and answers as they're being generated

## Architecture

The extension consists of two main components:

1. **Frontend**: Browser extension UI and interaction code
2. **Backend**: Flask server that handles text processing, embeddings, and LLM integration

### Technology Stack

- **Browser Extension**: JavaScript, HTML, CSS
- **Backend Server**: Python, Flask, CORS
- **LLM Integration**: Ollama (using llama3.2 model)
- **Vector Database**: FAISS for efficient similarity search
- **RAG Framework**: LangChain for document processing and retrieval chains

## Installation

### Prerequisites

- **Ollama**: Install [Ollama](https://ollama.ai/) and pull the llama3.2 model
- **Python**: Python 3.8+ with pip
- **Web Browser**: Firefox or Chrome

### Backend Setup

1. Clone this repository
```bash
git clone https://github.com/your-username/ai-buddy-extension.git
cd ai-buddy-extension
```
2. Install required Python packages
```bash
pip install flask flask-cors langchain-community langchain-ollama langchain faiss-cpu
```
3. Start the backend server
```bash
cd backend 
python main.py
```
The server will start on [http://localhost:5000](http://localhost:5000)
### Extension Installation

#### Firefox

1.  Open Firefox
2.  Enter `about:debugging` in the URL bar
3.  Click "This Firefox"
4.  Click "Load Temporary Add-on"
5.  Select the `manifest.json` file from the repository

#### Chrome

1.  Open Chrome
2.  Go to `chrome://extensions/`
3.  Enable "Developer mode"
4.  Click "Load unpacked"
5.  Select the root folder of the repository

## Usage

1.  Navigate to any webpage
2.  Click the AI Buddy extension icon in your browser toolbar
3.  Click "Extract Text" to generate a summary of the current page
4.  Type a question in the input field and click "Ask" to get answers about the page content
5.  Use "Clear Text" to reset the conversation for the current pageai-buddy-
## Project Structure
```bash
extension/
├── backend/
│   └── main.py             # Flask server with RAG implementation
├── frontend/
│   ├── background.js       # Extension background script
│   ├── icon.png            # Extension icon
│   ├── popup.html          # Extension popup UI
│   ├── popup.js            # Extension popup logic
│   ├── question.js         # Script to handle question answering
│   └── summary.js          # Script to handle text summarization
└── manifest.json           # Extension manifest file
```
## How It Works

1.  When the user clicks "Extract Text":
    -   The extension extracts all text from the current webpage
    -   The text is sent to the backend server
    -   The server processes the text and generates embeddings
    -   The LLM generates a summary which is streamed back to the extension
    -   The summary is displayed and stored for future reference
2.  When the user asks a question:
    -   The question and webpage text are sent to the backend
    -   The RAG system retrieves relevant context from the text
    -   The LLM generates an answer based on the retrieved context
    -   The answer is streamed back to the extension and displayed
## Development

### Backend Development

The backend server uses:

-   `Flask` for the web server
-   `langchain` for document processing and RAG implementation
-   `FAISS` for efficient vector search
-   `Ollama` for local LLM integration

Key components:

-   Text splitting and embedding generation
-   Vector store management for contextual retrieval
-   Streaming response handling for real-time feedback

### Extension Development

The extension uses:

-   Browser extension APIs for tab interaction and storage
-   Event-driven communication between components
-   SSE (Server-Sent Events) for streaming responses

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - [paawankarwa22@gmail.com](mailto:your-email@example.com)

Project Link: [https://github.com/karwap22/ragExtension](https://github.com/karwap22/ragExtension)
