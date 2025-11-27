# 🚀 Complete Deployment Guide for RAG Research Assistant

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [File Overview](#file-overview)
3. [Step-by-Step Deployment](#step-by-step-deployment)
4. [Troubleshooting](#troubleshooting)
5. [Adding Secrets](#adding-secrets)

---

## Prerequisites

Before you start, make sure you have:
- ✅ A GitHub account (free) - [Sign up here](https://github.com/signup)
- ✅ An OpenAI API key - [Get one here](https://platform.openai.com/api-keys)
- ✅ Downloaded all project files

---

## File Overview

Your project should have these files:

```
rag-research-assistant/
├── app.py                    ← Main application (DO NOT MODIFY)
├── requirements.txt          ← Python packages
├── packages.txt              ← System packages
├── README.md                 ← Documentation
├── .gitignore                ← Git ignore rules
└── .streamlit/
    └── config.toml           ← Theme configuration
```

---

## Step-by-Step Deployment

### 📌 STEP 1: Create a GitHub Repository

1. Go to **[github.com](https://github.com)** and sign in
2. Click the **+** button in the top-right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `rag-research-assistant`
   - **Description**: `AI-powered RAG system for research paper Q&A`
   - **Visibility**: Select **Public** ⚠️ (Required for free Streamlit Cloud)
   - **Initialize**: Leave all checkboxes UNCHECKED
5. Click **"Create repository"**

---

### 📌 STEP 2: Upload Files to GitHub

**Method A: Using GitHub Web Interface (Easiest)**

1. In your new repository page, click **"uploading an existing file"** link
   (Or click **Add file** → **Upload files**)

2. **Upload these files first:**
   - `app.py`
   - `requirements.txt`
   - `packages.txt`
   - `README.md`
   - `.gitignore`

3. Click **"Commit changes"**

4. **Create the .streamlit folder:**
   - Click **Add file** → **Create new file**
   - Type: `.streamlit/config.toml`
   - Copy-paste the contents of `config.toml`
   - Click **"Commit new file"**

**Method B: Using Git Command Line**

```bash
# 1. Clone your empty repository
git clone https://github.com/YOUR_USERNAME/rag-research-assistant.git

# 2. Navigate to the folder
cd rag-research-assistant

# 3. Copy all downloaded files here (app.py, requirements.txt, etc.)

# 4. Add all files
git add .

# 5. Commit
git commit -m "Add RAG Research Assistant app"

# 6. Push to GitHub
git push origin main
```

---

### 📌 STEP 3: Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**

2. Click **"Sign in with GitHub"** and authorize Streamlit

3. Click **"New app"** button

4. Fill in the deployment form:

   | Field | Value |
   |-------|-------|
   | Repository | `YOUR_USERNAME/rag-research-assistant` |
   | Branch | `main` |
   | Main file path | `app.py` |

5. Click **"Advanced settings"** (optional):
   - Python version: `3.11`

6. Click **"Deploy!"** 🚀

---

### 📌 STEP 4: Wait for Deployment

- The deployment process takes **2-5 minutes**
- You'll see a build log on screen
- When complete, you'll get a URL like:
  ```
  https://your-app-name.streamlit.app
  ```

---

### 📌 STEP 5: Add Your API Key (Optional but Recommended)

For security, add your OpenAI API key as a secret:

1. In your deployed app, click **"Manage app"** (bottom-right corner)
2. Click **"Settings"** → **"Secrets"**
3. Add:
   ```toml
   OPENAI_API_KEY = "sk-your-api-key-here"
   ```
4. Click **"Save"**

This way, you won't need to enter your API key every time!

---

## Troubleshooting

### ❌ Error: "ModuleNotFoundError"
**Solution**: Make sure `requirements.txt` is in your repository root

### ❌ Error: "sqlite3 not found"
**Solution**: This is handled by the `pysqlite3-binary` package in requirements.txt

### ❌ Error: "Application keeps restarting"
**Solution**: Check your API key is valid and has credits

### ❌ Files not showing after upload
**Solution**: Make sure you committed the changes after uploading

### ❌ ".streamlit folder not visible"
**Solution**: Hidden folders (starting with `.`) might not show in file browser.
Create it manually:
1. Click **Add file** → **Create new file**
2. Type: `.streamlit/config.toml`
3. Paste config content

---

## Using Your Deployed App

1. **Open your app URL**
2. **Enter your OpenAI API key** in the sidebar (if not set as secret)
3. **Upload PDF research papers** using the sidebar
4. **Wait for processing** (you'll see a spinner)
5. **Ask questions** about your papers!
6. **View sources** for each answer

---

## Sample Research Papers to Test

You can use these classic AI papers:
- "Attention Is All You Need" (Transformer paper)
- "Language Models are Few-Shot Learners" (GPT-3 paper)
- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- "BERT: Pre-training of Deep Bidirectional Transformers"

---

## Cost Considerations

- **Streamlit Cloud**: FREE for public repositories
- **OpenAI API**: Pay-per-use
  - `gpt-4o-mini`: ~$0.15 per 1M input tokens
  - `text-embedding-3-small`: ~$0.02 per 1M tokens

Typical cost for analyzing 3-4 research papers: **< $0.10**

---

## Need Help?

- Streamlit Documentation: [docs.streamlit.io](https://docs.streamlit.io)
- LangChain Documentation: [python.langchain.com](https://python.langchain.com)
- OpenAI API Reference: [platform.openai.com/docs](https://platform.openai.com/docs)

---

**Congratulations! 🎉 Your RAG Research Assistant is now live!**
