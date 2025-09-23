# 🧠 ClusterGen

ClusterGen is a powerful and modular GenAI application designed to simplify creative and analytical tasks like image generation, AI web scraping, audio chat, and real-time document processing using state-of-the-art language and vision models.

## 🚀 Features

### 🌐 AI Web Scraper
- Extract structured information from any webpage.
- Clean and readable outputs using LLM-backed parsing.

### 🖼️ Image Generation
- Leverages Hugging Face’s FLUX and LoRA models.
- High-quality, realistic image generation from prompts.
- Built-in prompt logging and filtering.

### 🎙️ Audio Chat
- Record and transcribe audio directly in-browser.
- Multi-modal support for text-to-speech and speech-to-text.

### 🧪 Temporary AI Playground
- Run temporary conversations with any OpenAI or Groq-compatible LLM.
- Fast inference via Groq's API integration.

## 📦 Tech Stack

- **Frontend**: Streamlit (with dark/light theme toggle)
- **Backend**: Python 3.12+, Hugging Face Transformers, LangChain
- **Models**:
  - FLUX for image gen
  - Whisper for audio
  - spaCy NER for redaction
  - GPT / Mixtral (via Groq) for LLM responses
- **Storage**: MongoDB (for prompt logging)
- **APIs**: Hugging Face Inference API, Groq API, OpenAI API
