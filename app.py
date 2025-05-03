import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import random

# Load environment variables
load_dotenv()

# Set page configuration with custom theme
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize dark mode in session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True  # Set dark mode as default

# Custom CSS for animations and styling
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }
    
    .main .block-container {
        max-width: 1200px;
        padding: 2rem 1rem;
    }
    
    .stTextInput>div>div>input {
        background: #2d2d2d;
        border-radius: 10px;
        border: 1px solid #3d3d3d;
        padding: 12px 15px;
        color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #2196F3;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
    }
    
    .stSelectbox>div>div>select {
        background: #2d2d2d;
        border-radius: 10px;
        border: 1px solid #3d3d3d;
        padding: 12px 15px;
        color: #ffffff;
    }
    
    .chat-message {
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        background: #2d2d2d;
        border: 1px solid #3d3d3d;
    }
    
    .chat-message.user {
        background: #2d2d2d;
        border-left: 4px solid #2196F3;
    }
    
    .chat-message.assistant {
        background: #2d2d2d;
        border-left: 4px solid #4CAF50;
    }
    
    .language-selector {
        background: #2d2d2d;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #3d3d3d;
    }
    
    .sidebar .sidebar-content {
        background: #1e1e1e;
        padding: 1rem;
    }
    
    .title-container {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
    }
    
    .title-container h1 {
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    
    .stButton>button {
        background: #2196F3;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: #1976D2;
        transform: translateY(-2px);
    }
    
    .theme-toggle button {
        background: #2d2d2d;
        border: 1px solid #3d3d3d;
        color: #ffffff;
    }
    
    .theme-toggle button:hover {
        background: #3d3d3d;
    }
    
    .stMarkdown {
        color: #ffffff;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffffff;
    }
    
    .stMarkdown p {
        color: #e0e0e0;
    }
    
    .stInfo, .stSuccess, .stError {
        background: #2d2d2d;
        border: 1px solid #3d3d3d;
        color: #ffffff;
    }
    
    .language-tab {
        background: #2d2d2d;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
        border: 1px solid #3d3d3d;
    }
    .language-tab:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        border-color: #2196F3;
    }
    .language-tab label {
        color: #ffffff;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .language-tab .stSelectbox > div {
        background: #2d2d2d;
        border-radius: 8px;
        border: 1px solid #3d3d3d;
    }
    .language-tab .stSelectbox > div:hover {
        border-color: #2196F3;
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .slide-in {
        animation: slideIn 0.5s ease-out forwards;
    }
    </style>
""", unsafe_allow_html=True)

# Validate API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    st.error("❌ API key not found. Please create a .env file with your GOOGLE_API_KEY.")
    st.stop()

try:
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    # Test the API connection
    model = genai.GenerativeModel('gemini-2.0-flash')
    model.generate_content("test")
except Exception as e:
    st.error(f"❌ Error connecting to Gemini API: {str(e)}")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "translation_history" not in st.session_state:
    st.session_state.translation_history = []
if "source" not in st.session_state:
    st.session_state.source = "English"
if "target" not in st.session_state:
    st.session_state.target = "Hindi"
if "last_translation" not in st.session_state:
    st.session_state.last_translation = None
if "swap_triggered" not in st.session_state:
    st.session_state.swap_triggered = False

# Handle language swap before creating widgets
if st.session_state.swap_triggered:
    st.session_state.source, st.session_state.target = st.session_state.target, st.session_state.source
    st.session_state.swap_triggered = False
    st.rerun()

# Sidebar
with st.sidebar:
    st.title("🌐 Language Translator")
    
    # Theme Toggle
    st.markdown('<div class="theme-toggle">', unsafe_allow_html=True)
    if st.button("🌙" if st.session_state.dark_mode else "☀️", key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Quick Tips")
    st.markdown("""
    - Select source and target languages
    - Type your text to translate
    - Use the swap button to switch languages
    - View your translation history
    - Click on history items to reuse them
    """)
    
    # Quick Language Presets
    st.markdown("### 🚀 Quick Presets")
    
    # English to Indian Languages
    st.markdown("#### 🇮🇳 English to Indian Languages")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("English → Hindi"):
            st.session_state.source = "English"
            st.session_state.target = "Hindi"
            st.rerun()
        if st.button("English → Punjabi"):
            st.session_state.source = "English"
            st.session_state.target = "Punjabi"
            st.rerun()
        if st.button("English → Marathi"):
            st.session_state.source = "English"
            st.session_state.target = "Marathi"
            st.rerun()
        if st.button("English → Tamil"):
            st.session_state.source = "English"
            st.session_state.target = "Tamil"
            st.rerun()
        if st.button("English → Telugu"):
            st.session_state.source = "English"
            st.session_state.target = "Telugu"
            st.rerun()
        if st.button("English → Sanskrit"):
            st.session_state.source = "English"
            st.session_state.target = "Sanskrit"
            st.rerun()

    with col2:
        if st.button("Hindi → English"):
            st.session_state.source = "Hindi"
            st.session_state.target = "English"
            st.rerun()
        if st.button("Punjabi → English"):
            st.session_state.source = "Punjabi"
            st.session_state.target = "English"
            st.rerun()
        if st.button("Marathi → English"):
            st.session_state.source = "Marathi"
            st.session_state.target = "English"
            st.rerun()
        if st.button("Tamil → English"):
            st.session_state.source = "Tamil"
            st.session_state.target = "English"
            st.rerun()
        if st.button("Telugu → English"):
            st.session_state.source = "Telugu"
            st.session_state.target = "English"
            st.rerun()
        if st.button("Sanskrit → English"):
            st.session_state.source = "Sanskrit"
            st.session_state.target = "English"
            st.rerun()

    # Indian Language Pairs
    st.markdown("#### 🔄 Indian Language Pairs")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Hindi → Punjabi"):
            st.session_state.source = "Hindi"
            st.session_state.target = "Punjabi"
            st.rerun()
        if st.button("Hindi → Marathi"):
            st.session_state.source = "Hindi"
            st.session_state.target = "Marathi"
            st.rerun()
        if st.button("Hindi → Tamil"):
            st.session_state.source = "Hindi"
            st.session_state.target = "Tamil"
            st.rerun()
        if st.button("Hindi → Bengali"):
            st.session_state.source = "Hindi"
            st.session_state.target = "Bengali"
            st.rerun()
        if st.button("Hindi → Sanskrit"):
            st.session_state.source = "Hindi"
            st.session_state.target = "Sanskrit"
            st.rerun()

    with col2:
        if st.button("Punjabi → Hindi"):
            st.session_state.source = "Punjabi"
            st.session_state.target = "Hindi"
            st.rerun()
        if st.button("Marathi → Hindi"):
            st.session_state.source = "Marathi"
            st.session_state.target = "Hindi"
            st.rerun()
        if st.button("Tamil → Hindi"):
            st.session_state.source = "Tamil"
            st.session_state.target = "Hindi"
            st.rerun()
        if st.button("Bengali → Hindi"):
            st.session_state.source = "Bengali"
            st.session_state.target = "Hindi"
            st.rerun()
        if st.button("Sanskrit → Hindi"):
            st.session_state.source = "Sanskrit"
            st.session_state.target = "Hindi"
            st.rerun()

    # English to International Languages
    st.markdown("#### 🌍 English to International Languages")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("English → French"):
            st.session_state.source = "English"
            st.session_state.target = "French"
            st.rerun()
        if st.button("English → German"):
            st.session_state.source = "English"
            st.session_state.target = "German"
            st.rerun()
        if st.button("English → Spanish"):
            st.session_state.source = "English"
            st.session_state.target = "Spanish"
            st.rerun()
        if st.button("English → Japanese"):
            st.session_state.source = "English"
            st.session_state.target = "Japanese"
            st.rerun()
        if st.button("English → Chinese"):
            st.session_state.source = "English"
            st.session_state.target = "Chinese"
            st.rerun()

    with col2:
        if st.button("French → English"):
            st.session_state.source = "French"
            st.session_state.target = "English"
            st.rerun()
        if st.button("German → English"):
            st.session_state.source = "German"
            st.session_state.target = "English"
            st.rerun()
        if st.button("Spanish → English"):
            st.session_state.source = "Spanish"
            st.session_state.target = "English"
            st.rerun()
        if st.button("Japanese → English"):
            st.session_state.source = "Japanese"
            st.session_state.target = "English"
            st.rerun()
        if st.button("Chinese → English"):
            st.session_state.source = "Chinese"
            st.session_state.target = "English"
            st.rerun()

    # International Language Pairs
    st.markdown("#### 🔄 International Language Pairs")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("French → German"):
            st.session_state.source = "French"
            st.session_state.target = "German"
            st.rerun()
        if st.button("Spanish → French"):
            st.session_state.source = "Spanish"
            st.session_state.target = "French"
            st.rerun()
        if st.button("Japanese → Korean"):
            st.session_state.source = "Japanese"
            st.session_state.target = "Korean"
            st.rerun()
        if st.button("Chinese → Japanese"):
            st.session_state.source = "Chinese"
            st.session_state.target = "Japanese"
            st.rerun()

    with col2:
        if st.button("German → French"):
            st.session_state.source = "German"
            st.session_state.target = "French"
            st.rerun()
        if st.button("French → Spanish"):
            st.session_state.source = "French"
            st.session_state.target = "Spanish"
            st.rerun()
        if st.button("Korean → Japanese"):
            st.session_state.source = "Korean"
            st.session_state.target = "Japanese"
            st.rerun()
        if st.button("Japanese → Chinese"):
            st.session_state.source = "Japanese"
            st.session_state.target = "Chinese"
            st.rerun()

    # Indian to International Languages
    st.markdown("#### 🌐 Indian to International Languages")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Hindi → French"):
            st.session_state.source = "Hindi"
            st.session_state.target = "French"
            st.rerun()
        if st.button("Hindi → German"):
            st.session_state.source = "Hindi"
            st.session_state.target = "German"
            st.rerun()
        if st.button("Hindi → Spanish"):
            st.session_state.source = "Hindi"
            st.session_state.target = "Spanish"
            st.rerun()
        if st.button("Hindi → Japanese"):
            st.session_state.source = "Hindi"
            st.session_state.target = "Japanese"
            st.rerun()

    with col2:
        if st.button("French → Hindi"):
            st.session_state.source = "French"
            st.session_state.target = "Hindi"
            st.rerun()
        if st.button("German → Hindi"):
            st.session_state.source = "German"
            st.session_state.target = "Hindi"
            st.rerun()
        if st.button("Spanish → Hindi"):
            st.session_state.source = "Spanish"
            st.session_state.target = "Hindi"
            st.rerun()
        if st.button("Japanese → Hindi"):
            st.session_state.source = "Japanese"
            st.session_state.target = "Hindi"
            st.rerun()

    st.markdown("---")
    # Translation History
    st.markdown("### 📚 Translation History")
    if st.session_state.translation_history:
        for idx, item in enumerate(reversed(st.session_state.translation_history[-5:])):
            if st.button(f"From: {item['source']} → {item['target']}\nText: {item['original'][:30]}...", 
                        key=f"history_{idx}",
                        help="Click to reuse this translation"):
                st.session_state.source = item['source']
                st.session_state.target = item['target']
                st.session_state.last_translation = item
                st.rerun()
    else:
        st.info("No translation history yet")

# Main content
st.markdown('<div class="title-container fade-in">', unsafe_allow_html=True)
st.markdown("<h1>🌐 AI Language Translator</h1>", unsafe_allow_html=True)
st.markdown("""
    <div class='fade-in'>
        <p style="text-align: center; font-size: 1.2rem;">Translate text between different languages instantly using the power of AI!</p>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Language selection with enhanced UI
col1, col2, col3 = st.columns([1, 1, 0.2])
with col1:
    source_lang = st.selectbox(
        "Source Language",
        [
            # Indian Languages
            "Hindi", "Bengali", "Punjabi", "Marathi", "Gujarati", "Tamil", 
            "Telugu", "Kannada", "Malayalam", "Odia", "Assamese", "Urdu",
            "Bhojpuri", "Rajasthani", "Haryanvi", "Kashmiri", "Sindhi", "Sanskrit",
            
            # Global Languages
            "English", "Spanish", "French", "German", "Italian", "Portuguese", 
            "Russian", "Japanese", "Chinese", "Korean", "Arabic", "Turkish", 
            "Dutch", "Swedish", "Greek", "Polish", "Vietnamese", "Thai", 
            "Indonesian", "Malay", "Hebrew", "Persian", "Czech", "Danish",
            "Finnish", "Hungarian", "Norwegian", "Romanian", "Slovak",
            "Ukrainian", "Bulgarian", "Croatian", "Estonian", "Icelandic",
            "Latvian", "Lithuanian", "Macedonian", "Serbian", "Slovenian"
        ],
        key="source_select",
        index=[
            # Indian Languages
            "Hindi", "Bengali", "Punjabi", "Marathi", "Gujarati", "Tamil", 
            "Telugu", "Kannada", "Malayalam", "Odia", "Assamese", "Urdu",
            "Bhojpuri", "Rajasthani", "Haryanvi", "Kashmiri", "Sindhi", "Sanskrit",
            
            # Global Languages
            "English", "Spanish", "French", "German", "Italian", "Portuguese", 
            "Russian", "Japanese", "Chinese", "Korean", "Arabic", "Turkish", 
            "Dutch", "Swedish", "Greek", "Polish", "Vietnamese", "Thai", 
            "Indonesian", "Malay", "Hebrew", "Persian", "Czech", "Danish",
            "Finnish", "Hungarian", "Norwegian", "Romanian", "Slovak",
            "Ukrainian", "Bulgarian", "Croatian", "Estonian", "Icelandic",
            "Latvian", "Lithuanian", "Macedonian", "Serbian", "Slovenian"
        ].index(st.session_state.source)
    )

with col2:
    target_lang = st.selectbox(
        "Target Language",
        [
            # Indian Languages
            "Hindi", "Bengali", "Punjabi", "Marathi", "Gujarati", "Tamil", 
            "Telugu", "Kannada", "Malayalam", "Odia", "Assamese", "Urdu",
            "Bhojpuri", "Rajasthani", "Haryanvi", "Kashmiri", "Sindhi", "Sanskrit",
            
            # Global Languages
            "English", "Spanish", "French", "German", "Italian", "Portuguese", 
            "Russian", "Japanese", "Chinese", "Korean", "Arabic", "Turkish", 
            "Dutch", "Swedish", "Greek", "Polish", "Vietnamese", "Thai", 
            "Indonesian", "Malay", "Hebrew", "Persian", "Czech", "Danish",
            "Finnish", "Hungarian", "Norwegian", "Romanian", "Slovak",
            "Ukrainian", "Bulgarian", "Croatian", "Estonian", "Icelandic",
            "Latvian", "Lithuanian", "Macedonian", "Serbian", "Slovenian"
        ],
        key="target_select",
        index=[
            # Indian Languages
            "Hindi", "Bengali", "Punjabi", "Marathi", "Gujarati", "Tamil", 
            "Telugu", "Kannada", "Malayalam", "Odia", "Assamese", "Urdu",
            "Bhojpuri", "Rajasthani", "Haryanvi", "Kashmiri", "Sindhi", "Sanskrit",
            
            # Global Languages
            "English", "Spanish", "French", "German", "Italian", "Portuguese", 
            "Russian", "Japanese", "Chinese", "Korean", "Arabic", "Turkish", 
            "Dutch", "Swedish", "Greek", "Polish", "Vietnamese", "Thai", 
            "Indonesian", "Malay", "Hebrew", "Persian", "Czech", "Danish",
            "Finnish", "Hungarian", "Norwegian", "Romanian", "Slovak",
            "Ukrainian", "Bulgarian", "Croatian", "Estonian", "Icelandic",
            "Latvian", "Lithuanian", "Macedonian", "Serbian", "Slovenian"
        ].index(st.session_state.target)
    )

with col3:
    st.markdown("""
        <style>
            .swap-button {
                background: #2196F3;
                color: white;
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-top: 2rem;
            }
            .swap-button:hover {
                background: #1976D2;
                transform: scale(1.1);
            }
        </style>
    """, unsafe_allow_html=True)
    if st.button("🔄", key="swap_button", help="Swap languages"):
        st.session_state.swap_triggered = True
        st.rerun()

# Update session state if languages changed
if source_lang != st.session_state.source or target_lang != st.session_state.target:
    st.session_state.source = source_lang
    st.session_state.target = target_lang
    st.rerun()

# Chat input with enhanced UI
st.markdown("""
    <style>
        .stChatInputContainer {
            background: #2d2d2d;
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
        }
        .stChatInputTextArea {
            background: #2d2d2d !important;
            border: 1px solid #3d3d3d !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            padding: 12px 15px !important;
            font-size: 1rem !important;
            min-height: 100px !important;
            resize: vertical !important;
        }
        .stChatInputTextArea:focus {
            border-color: #2196F3 !important;
            box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2) !important;
        }
        .stChatInputTextArea::placeholder {
            color: #888888 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Display last translation if available
if st.session_state.last_translation:
    st.info(f"Last translation: {st.session_state.last_translation['original']} → {st.session_state.last_translation['translation']}")

if prompt := st.chat_input("Enter your text to translate"):
    # Add user message to chat history with animation
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Create the translation prompt
        translation_prompt = f"""
        Translate the following text from {source_lang} to {target_lang}:
        {prompt}
        
        Please provide only the translation without any additional explanation.
        """
        
        # Get response from Gemini with loading animation
        with st.spinner("Translating..."):
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(translation_prompt)
            
            # Add to translation history
            translation_item = {
                "source": source_lang,
                "target": target_lang,
                "original": prompt,
                "translation": response.text
            }
            st.session_state.translation_history.append(translation_item)
            st.session_state.last_translation = translation_item
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            # Success animation
            st.success("Translation complete!")
            
    except Exception as e:
        st.error(f"❌ Error during translation: {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error while translating. Please try again."})

# Display chat history with enhanced UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"""
            <div class="chat-message {'user' if message['role'] == 'user' else 'assistant'}">
                {message['content']}
            </div>
        """, unsafe_allow_html=True)

# Footer with enhanced UI
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="font-size: 1.1rem;">Made by</p>
        <p style="font-size: 1.1rem;">RAJAT RAJAN</p>
        <p style="font-size: 1.1rem;">✨ Fast and accurate translations ✨</p>
    </div>
""", unsafe_allow_html=True) 