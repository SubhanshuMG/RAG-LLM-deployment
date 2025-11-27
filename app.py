try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- Page Config ---
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Attractive UI ---
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles - Dark Theme */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(180deg, #0d0d1a 0%, #1a1a2e 100%);
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Global text color */
    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #e0e0e0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        border: 2px dashed rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Chat container - Dark Theme */
    .chat-container {
        background: #1a1a2e;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
    }
    
    /* Chat messages - Dark Theme */
    .stChatMessage {
        background: #1e1e2e !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        margin-bottom: 1rem !important;
        border: 1px solid #3d3d5c !important;
    }
    
    [data-testid="stChatMessageContent"] {
        font-size: 1rem;
        line-height: 1.7;
        color: #e0e0e0 !important;
    }
    
    [data-testid="stChatMessageContent"] p {
        color: #e0e0e0 !important;
    }
    
    /* User message styling */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, #4a4a6a 0%, #3d3d5c 100%) !important;
        border: 1px solid #667eea !important;
    }
    
    /* Assistant message styling */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%) !important;
        border: 1px solid #3d3d5c !important;
    }
    
    /* Avatar containers */
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        background: #2a2a3e !important;
        border-radius: 8px !important;
    }
    
    /* Source card styling - Dark Theme */
    .source-card {
        background: linear-gradient(135deg, #2a2a3e 0%, #1e1e2e 100%);
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0 12px 12px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #c0c0c0;
    }
    
    .source-card strong {
        color: #667eea;
    }
    
    .source-card small {
        color: #a0a0a0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Info box styling - Dark Theme */
    .info-box {
        background: linear-gradient(135deg, #1a3a4a 0%, #0d2836 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #00bcd4;
        color: #b0e0e6;
    }
    
    .info-box h4 {
        color: #00e5ff;
        margin-bottom: 0.5rem;
    }
    
    .info-box p {
        color: #b0e0e6;
    }
    
    .info-box a {
        color: #667eea;
    }
    
    /* Success box - Dark Theme */
    .success-box {
        background: linear-gradient(135deg, #1a3a2a 0%, #0d2818 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #4caf50;
        color: #a8e6cf;
    }
    
    /* Stats cards - Dark Theme */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        flex: 1;
        border: 1px solid #3d3d5c;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #a0a0a0;
    }
    
    /* Feature cards - Dark Theme */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        border: 1px solid #3d3d5c;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
        border-color: #667eea;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-weight: 600;
        color: #e0e0e0;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.85rem;
        color: #a0a0a0;
    }
    
    /* Chat input styling - Dark Theme */
    .stChatInput {
        border-radius: 12px;
    }
    
    .stChatInput > div {
        border-radius: 12px !important;
        border: 2px solid #3d3d5c !important;
        background: #1e1e2e !important;
    }
    
    .stChatInput > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stChatInput textarea {
        color: #e0e0e0 !important;
        background: transparent !important;
    }
    
    .stChatInput textarea::placeholder {
        color: #808080 !important;
    }
    
    /* Divider - Dark Theme */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    /* Expander styling - Dark Theme */
    .streamlit-expanderHeader {
        background: #2a2a3e !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
    }
    
    .streamlit-expanderContent {
        background: #1e1e2e !important;
        border: 1px solid #3d3d5c !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }
    
    [data-testid="stExpander"] {
        background: transparent !important;
        border: 1px solid #3d3d5c !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stExpander"] summary {
        color: #a0a0a0 !important;
    }
    
    [data-testid="stExpander"] summary:hover {
        color: #667eea !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .feature-grid {
            grid-template-columns: 1fr 1fr;
        }
        
        .stats-container {
            flex-direction: column;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>[AI Research Assistant]</h1>
    <p>Upload research papers and get intelligent answers with source citations
    <b><h4><i>by</i> Subhanshu Mohan Gupta</h4></b></p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")
    
    # API Key Input
    st.markdown("### 🔑 API Key")
    user_api_key = st.text_input(
        "Enter OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Get your API key from platform.openai.com"
    )
    
    st.markdown("---")
    
    # Model Selection
    st.markdown("### 🤖 Model Settings")
    model_choice = st.selectbox(
        "Select Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0,
        help="Choose the AI model for generating responses"
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        help="Higher values make output more creative, lower values more focused"
    )
    
    st.markdown("---")
    
    # Retrieval Settings
    st.markdown("### 🔍 Retrieval Settings")
    chunk_size = st.slider(
        "Chunk Size",
        min_value=500,
        max_value=5000,
        value=3000,
        step=500,
        help="Size of text chunks for processing"
    )
    
    top_k = st.slider(
        "Top K Results",
        min_value=1,
        max_value=10,
        value=3,
        help="Number of relevant chunks to retrieve"
    )
    
    st.markdown("---")
    
    # File Uploader
    st.markdown("### 📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Drop your PDFs here",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDF research papers"
    )
    
    if uploaded_files:
        st.markdown(f"""
        <div style="background: rgba(102, 126, 234, 0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong>📚 {len(uploaded_files)} file(s) uploaded</strong>
        </div>
        """, unsafe_allow_html=True)
        
        for file in uploaded_files:
            st.markdown(f"• {file.name}")
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state["messages"] = []
        st.session_state["messages"].append({
            "role": "assistant",
            "content": "Chat cleared! Ask me anything about your documents."
        })
        st.rerun()
    
    # About section
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; opacity: 0.7;">
        <small>
            Built with ❤️ using<br>
            Streamlit • LangChain • OpenAI
        </small>
    </div>
    """, unsafe_allow_html=True)


# --- Backend Functions ---

def process_documents(uploaded_files, chunk_size):
    """Process and vectorize uploaded documents."""
    all_docs = []
    file_names = []
    
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_file_path = tmp_file.name

        try:
            loader = PyMuPDFLoader(temp_file_path)
            docs = loader.load()
            
            # Add source metadata
            for doc in docs:
                doc.metadata["source"] = uploaded_file.name
            
            all_docs.extend(docs)
            file_names.append(uploaded_file.name)
        finally:
            os.remove(temp_file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=300,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    doc_chunks = splitter.split_documents(all_docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    vectorstore = Chroma.from_documents(
        documents=doc_chunks,
        collection_name="rag_collection",
        embedding=embeddings,
    )
    
    return vectorstore, len(doc_chunks), file_names


def get_rag_chain_with_sources(vectorstore, model_name, temperature, top_k):
    """Create RAG chain with source attribution."""
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k}
    )
    
    rag_prompt = """You are an expert AI research assistant specializing in analyzing academic papers.
    Answer the question based ONLY on the provided context from research papers.
    
    IMPORTANT GUIDELINES:
    - Provide detailed, well-structured answers
    - Use technical terminology appropriately
    - If information is not in the context, clearly state "I don't have information about this in the provided documents"
    - Reference specific sections or concepts from the papers when relevant
    - Use bullet points and formatting for clarity when appropriate
    
    Question: {question}
    
    Context from Research Papers:
    {context}
    
    Detailed Answer:"""
    
    rag_prompt_template = ChatPromptTemplate.from_template(rag_prompt)
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    
    def format_docs(docs):
        formatted = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "N/A")
            formatted.append(f"[Source {i+1}: {source}, Page {page}]\n{doc.page_content}")
        return "\n\n---\n\n".join(formatted)
    
    def get_response_with_sources(question):
        # Get relevant documents
        docs = retriever.invoke(question)
        
        # Format context
        context = format_docs(docs)
        
        # Get response
        chain = rag_prompt_template | llm | StrOutputParser()
        response = chain.invoke({"question": question, "context": context})
        
        # Extract source info
        sources = []
        for doc in docs:
            source_info = {
                "file": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "N/A"),
                "preview": doc.page_content[:200] + "..."
            }
            sources.append(source_info)
        
        return response, sources
    
    return get_response_with_sources


# --- Main App Logic ---

# Check API Key
if user_api_key:
    os.environ["OPENAI_API_KEY"] = user_api_key
elif "OPENAI_API_KEY" not in os.environ:
    # Welcome screen when no API key
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Upload Papers</div>
            <div class="feature-desc">Support for multiple PDF research papers</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Smart Retrieval</div>
            <div class="feature-desc">Advanced vector search for accurate answers</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Powered</div>
            <div class="feature-desc">GPT-4 for intelligent response generation</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">Source Citation</div>
            <div class="feature-desc">Every answer includes source references</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4>🚀 Get Started</h4>
        <p>Enter your OpenAI API key in the sidebar to begin analyzing your research papers.</p>
        <p><small>Don't have an API key? Get one at <a href="https://platform.openai.com" target="_blank">platform.openai.com</a></small></p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Handle File Processing
if uploaded_files:
    # Check if files have changed
    current_files = [f.name for f in uploaded_files]
    if "processed_files" not in st.session_state or st.session_state["processed_files"] != current_files:
        with st.spinner(f"🔄 Processing {len(uploaded_files)} document(s)..."):
            try:
                vectorstore, num_chunks, file_names = process_documents(uploaded_files, chunk_size)
                st.session_state["vectorstore"] = vectorstore
                st.session_state["num_chunks"] = num_chunks
                st.session_state["file_names"] = file_names
                st.session_state["processed_files"] = current_files
                
                # Reset chat on new documents
                st.session_state["messages"] = [{
                    "role": "assistant",
                    "content": f"✅ Successfully processed {len(uploaded_files)} document(s) into {num_chunks} searchable chunks. Ask me anything about your research papers!"
                }]
                
            except Exception as e:
                st.error(f"❌ Error processing documents: {e}")
                st.stop()
    
    # Show stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(uploaded_files)}</div>
            <div class="stat-label">Documents</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.get('num_chunks', 0)}</div>
            <div class="stat-label">Text Chunks</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{top_k}</div>
            <div class="stat-label">Sources per Query</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
else:
    # No files uploaded
    st.markdown("""
    <div class="info-box">
        <h4>📤 Upload Your Research Papers</h4>
        <p>Use the sidebar to upload one or more PDF documents. The system will process them and enable intelligent Q&A.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample questions
    st.markdown("### 💡 Sample Questions You Can Ask")
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-desc">"What are the main components of a RAG model?"</div>
        </div>
        <div class="feature-card">
            <div class="feature-desc">"Explain the Transformer architecture"</div>
        </div>
        <div class="feature-card">
            <div class="feature-desc">"What is few-shot learning in GPT-3?"</div>
        </div>
        <div class="feature-card">
            <div class="feature-desc">"How does multi-head attention work?"</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "assistant",
        "content": "👋 Hi! I've analyzed your documents. Ask me any question about the research papers!"
    }]

# Display Chat Messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"], avatar="🧠" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])
        
        # Display sources if available
        if "sources" in msg and msg["sources"]:
            with st.expander("📚 View Sources", expanded=False):
                for i, source in enumerate(msg["sources"]):
                    st.markdown(f"""
                    <div class="source-card">
                        <strong>Source {i+1}:</strong> {source['file']} (Page {source['page']})<br>
                        <small>{source['preview']}</small>
                    </div>
                    """, unsafe_allow_html=True)

# Handle User Input
user_input = st.chat_input("Ask a question about your research papers...")

if user_input:
    # Display user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Generate Response
    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("🔍 Searching documents and generating response..."):
            try:
                vectorstore = st.session_state["vectorstore"]
                rag_function = get_rag_chain_with_sources(
                    vectorstore, model_choice, temperature, top_k
                )
                
                response, sources = rag_function(user_input)
                
                st.markdown(response)
                
                # Display sources
                with st.expander("📚 View Sources", expanded=False):
                    for i, source in enumerate(sources):
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>Source {i+1}:</strong> {source['file']} (Page {source['page']})<br>
                            <small>{source['preview']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Save to history
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": response,
                    "sources": sources
                })
                
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")