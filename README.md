# AI-Powered Language Translator

A modern, AI-powered language translation application built with Streamlit and Google's Gemini AI. This application provides real-time translation between multiple languages with a beautiful dark theme interface.

## 🌟 Features

- **AI-Powered Translation**: Uses Google's Gemini AI for accurate translations
- **Extensive Language Support**:
  - Indian Languages: Hindi, Bengali, Punjabi, Marathi, Gujarati, Tamil, Telugu, Kannada, Malayalam, Odia, Assamese, Urdu, Bhojpuri, Rajasthani, Haryanvi, Kashmiri, Sindhi, Sanskrit
  - Global Languages: English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Chinese, Korean, Arabic, and many more
- **User-Friendly Interface**:
  - Dark theme with smooth animations
  - Easy language selection
  - Quick language swap functionality
  - Translation history
  - Quick language presets
- **Smart Features**:
  - Real-time translation
  - Translation history tracking
  - Error handling
  - Loading animations
  - Responsive design

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## 📝 Usage

1. Run the application:
```bash
streamlit run app.py
```

2. Using the Translator:
   - Select source and target languages from the dropdown menus
   - Enter text to translate in the input field
   - View the translated text with animations
   - Use the swap button (🔄) to quickly switch between languages
   - Access translation history in the sidebar
   - Use quick presets for common language pairs

3. Features:
   - **Language Selection**: Choose from 40+ languages
   - **Quick Swap**: Swap languages with a single click
   - **Translation History**: View and reuse past translations
   - **Quick Presets**: Access common language pairs easily
   - **Dark Theme**: Comfortable viewing experience

## 🛠️ Technical Details

- **Backend**: Python with Streamlit
- **AI Model**: Google's Gemini AI
- **Frontend**: Streamlit with custom CSS
- **State Management**: Streamlit session state
- **Error Handling**: Comprehensive error management
- **Animations**: CSS-based smooth transitions

## 📚 Requirements

- Python 3.7+
- Streamlit
- google-generativeai
- python-dotenv
- Other dependencies listed in requirements.txt

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google for the Gemini AI model
- Streamlit for the web framework
- All contributors and users of the application 