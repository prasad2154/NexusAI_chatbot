import streamlit as st
import requests
import time

# Page configuration
st.set_page_config(
    page_title="NexusAI - Universal Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS (Glassmorphic dark-mode inspired design)
st.markdown(
    """
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Card container */
    .chat-header-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Metric Badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.3);
    }

    /* Quick Prompt Buttons */
    .stButton>button {
        background: rgba(255, 255, 255, 0.05);
        color: #e2e8f0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: #ffffff;
        border-color: transparent;
        transform: translateY(-2px);
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
    }

    /* Chat Messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        margin-bottom: 0.8rem;
    }

    /* Input area */
    .stChatInput > div {
        border-radius: 16px !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
        background: rgba(15, 23, 42, 0.8) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data(ttl=60)
def get_available_models(host_url):
    model_options = ["llama3.2:latest", "llama3", "mistral", "phi3", "gemma"]
    try:
        headers = {"Bypass-Tunnel-Remainder": "true", "User-Agent": "Mozilla/5.0"}
        r = requests.get(f"{host_url.rstrip('/')}/api/tags", headers=headers, timeout=1.5)
        if r.status_code == 200:
            fetched_models = [m['name'] for m in r.json().get('models', [])]
            if fetched_models:
                return fetched_models
    except Exception:
        pass
    return model_options

# Sidebar Configuration & Features
with st.sidebar:
    st.title("⚡ NexusAI")
    st.caption("Universal AI Assistant Platform")
    
    st.markdown("---")
    
    # Default Ollama Host URL (can be set to environment variable or public tunnel)
    default_url = "http://localhost:11434"
    ollama_host = st.text_input("Ollama Host URL", value=default_url, help="Set your public Ollama URL here so all users can connect automatically.")

    
    # Fetch cached models
    model_options = get_available_models(ollama_host)



    selected_model = st.selectbox("Select AI Model", model_options, index=0)
    
    system_persona = st.selectbox(
        "AI Personality",
        ["Default Assistant", "Coding Expert 🧑‍💻", "Creative Writer ✍️", "Concise & Fast ⚡"]
    )
    
    st.markdown("---")
    
    # Check if running on cloud vs local
    if "localhost" in ollama_host or "127.0.0.1" in ollama_host:
        st.warning("⚠️ **Cloud Notice**: You are on a cloud deployment (Streamlit Cloud). `localhost` refers to Streamlit's cloud server, NOT your local computer. Enter your Ngrok/tunnel URL below!")
    
    # System Status Indicator
    st.markdown('<span class="status-badge">● Engine Online</span>', unsafe_allow_html=True)
    st.write("")
    
    # Clear Chat Button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.info("🌐 **Remote Access**: Connect to your local Ollama using an `ngrok` or `localtunnel` URL in the host input above.")


# Header Section
col1, col2 = st.columns([3, 1])
with col1:
    st.title("⚡ NexusAI Assistant")
    st.markdown("Ask anything, brainstorm ideas, write code, or analyze text.")
with col2:
    st.metric(label="Selected Engine", value=selected_model.split(':')[0].upper())

# Pre-built Quick Interactive Prompts
st.markdown("##### 💡 Try Quick Suggestions:")
p_col1, p_col2, p_col3, p_col4 = st.columns(4)

prompt_clicked = None
if p_col1.button("🐍 Python Script", use_container_width=True):
    prompt_clicked = "Write a Python script to scrape website title and headlines using BeautifulSoup."
if p_col2.button("💡 Brainstorm Ideas", use_container_width=True):
    prompt_clicked = "Give me 5 unique startup ideas using Generative AI in healthcare."
if p_col3.button("📝 Summarize Text", use_container_width=True):
    prompt_clicked = "Explain Quantum Computing in 3 simple bullet points for a 10 year old."
if p_col4.button("🚀 Write an Email", use_container_width=True):
    prompt_clicked = "Write a polite follow-up email after a job interview."

# Initialise session state with welcome message
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Welcome to **NexusAI**! How can I assist you today? Feel free to pick a quick suggestion above or type your prompt below."}
    ]

# Render existing message history
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Capture Input from chat bar OR quick suggestion button
user_input = st.chat_input("Message NexusAI...")
if prompt_clicked:
    user_input = prompt_clicked

if user_input:
    # Append & display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Prepare message payload including optional persona instructions
    api_messages = []
    
    # Inject system prompt according to chosen persona
    if system_persona == "Coding Expert 🧑‍💻":
        api_messages.append({"role": "system", "content": "You are an expert software developer. Provide clean, well-commented code."})
    elif system_persona == "Creative Writer ✍️":
        api_messages.append({"role": "system", "content": "You are a creative writer. Use engaging, descriptive language."})
    elif system_persona == "Concise & Fast ⚡":
        api_messages.append({"role": "system", "content": "Be extremely brief, precise, and straight to the point."})
    
    # Add chat history
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    # Query Ollama model
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner(f"NexusAI ({selected_model}) is thinking..."):
            try:
                endpoint = f"{ollama_host.rstrip('/')}/api/chat"
                payload = {
                    "model": selected_model,
                    "messages": api_messages,
                    "stream": True
                }
                
                # Bypass localtunnel reminder page headers
                headers = {
                    "Bypass-Tunnel-Remainder": "true",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }
                
                # Streaming response for smooth interactive typing effect
                res = requests.post(endpoint, json=payload, headers=headers, stream=True, timeout=120)
                res.raise_for_status()

                
                import json
                for line in res.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        chunk_text = chunk.get("message", {}).get("content", "")
                        full_response += chunk_text
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                # If connection to Ollama fails on a deployed cloud instance, attempt fallback or clear demo guidance
                err_str = str(e)
                if "Connection refused" in err_str or "Max retries exceeded" in err_str:
                    full_response = (
                        f"⚠️ **Engine Disconnected**\n\n"
                        f"Your cloud app (`Streamlit Cloud`) tried connecting to `http://localhost:11434`, "
                        f"which is on your local PC.\n\n"
                        f"**How to enable live responses on your deployed link:**\n"
                        f"1. Run `npx localtunnel --port 11434` in your PC terminal.\n"
                        f"2. Paste the generated `https://...` link into the **Ollama Host URL** in the left sidebar.\n\n"
                        f"*Alternative*: If you are testing locally, launch `ollama serve` on your computer."
                    )
                else:
                    full_response = f"⚠️ **Error connecting to engine**: {e}"
                
                message_placeholder.markdown(full_response)


    # Store assistant response in history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
