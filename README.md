# 🧠 AI Research Assistant - RAG QA System

A powerful Retrieval-Augmented Generation (RAG) system for Question Answering on AI research papers. Built with Streamlit, LangChain, and OpenAI.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-green.svg)

## ✨ Features

- **📄 Document Preprocessing**: Load, chunk, and vectorize multiple PDF research papers
- **🔍 Smart Retrieval**: Optimized vector search using ChromaDB for handling complex queries
- **🤖 AI-Powered Answers**: Integration with GPT-4 for intelligent, context-aware responses
- **📚 Source Attribution**: Every answer includes references to the source documents and pages
- **🎨 Modern UI**: Beautiful, responsive interface with gradient themes
- **⚙️ Customizable Settings**: Adjust model, temperature, chunk size, and retrieval parameters

## 🚀 Deployment Guide

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** icon → **New repository**
3. Name it: `rag-research-assistant`
4. Set to **Public** (required for free Streamlit Cloud)
5. Click **Create repository**

### Step 2: Upload Files to GitHub

**Option A: Using GitHub Web Interface**

1. In your new repository, click **Add file** → **Upload files**
2. Upload these files:
   - `app.py`
   - `requirements.txt`
3. Create `.streamlit` folder and upload `config.toml`
4. Commit the changes

**Option B: Using Git Command Line**

```bash
# Clone your empty repository
git clone https://github.com/YOUR_USERNAME/rag-research-assistant.git
cd rag-research-assistant

# Copy your project files here, then:
git add .
git commit -m "Initial commit - RAG Research Assistant"
git push origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **Sign in with GitHub**
3. Click **New app**
4. Fill in the deployment settings:
   - **Repository**: `YOUR_USERNAME/rag-research-assistant`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **Deploy!**

### Step 4: Wait for Deployment

- Streamlit will install dependencies and build your app
- This typically takes 2-5 minutes
- Once complete, you'll get a URL like: `https://your-app-name.streamlit.app`

## 📁 Project Structure

```
rag-research-assistant/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## 🔧 Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| Model | GPT model for responses | gpt-4o-mini |
| Temperature | Response creativity (0-1) | 0.0 |
| Chunk Size | Text chunk size for processing | 3000 |
| Top K | Number of sources to retrieve | 3 |

## 📝 Sample Questions

1. What are the main components of a RAG model, and how do they interact?
2. What are the two sub-layers in each encoder layer of the Transformer model?
3. Explain how positional encoding is implemented in Transformers and why it is necessary.
4. Describe the concept of multi-head attention in the Transformer architecture. Why is it beneficial?
5. What is few-shot learning, and how does GPT-3 implement it during inference?

## 🛠️ Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/rag-research-assistant.git
cd rag-research-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

## 🔑 API Key

This application requires an OpenAI API key. You can:

1. Enter it in the sidebar when using the app
2. Set it as an environment variable: `OPENAI_API_KEY`
3. For Streamlit Cloud, add it in **App Settings** → **Secrets**:
   ```toml
   OPENAI_API_KEY = "sk-your-api-key-here"
   ```

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Built with ❤️ using Streamlit, LangChain, and OpenAI
