# 📝 Text Extractor - Browser Extension and API

## 📚 Introduction
Text Extractor is a Chrome/Firefox extension that extracts text from a webpage, summarizes it using a Flask backend integrated with an AI model (Ollama), and answers user queries based on the content of the webpage. It combines a browser extension with a REST API that handles text processing, embeddings, and retrieval.

## 📖 Table of Contents
- [Introduction](#-introduction)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Configuration](#-configuration)
- [Dependencies](#-dependencies)
- [Troubleshooting](#-troubleshooting)
- [Contributors](#-contributors)
- [License](#-license)

---

## ✨ Features
- Extract text from any webpage using the browser extension.
- Summarize extracted text using a Flask backend with LangChain and Ollama.
- Ask context-aware questions about the extracted content.
- Persistent storage of answers and summaries for each webpage.
- Real-time streaming responses for summaries and answers.

---

## 🛠️ Installation

### 📦 Backend Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/text-extractor.git
   cd text-extractor
