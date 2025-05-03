# AI Chat Assistant (ChatGPT Clone)

A simple ChatGPT-style AI agent website with a clean and modern UI/UX, built using only HTML, CSS, and Python (Flask). This application integrates with free AI models like Google's Gemini, HuggingFace's models, and optionally OpenAI's API.

## Features

- Clean, modern UI similar to ChatGPT
- Responsive design that works on desktop and mobile
- Integration with multiple AI models:
  - Google's Gemini API (free tier available)
  - HuggingFace's hosted models (free tier available)
  - OpenAI's API (optional)
- Fallback to predefined responses if no API keys are configured
- Example prompts to get started
- Animated typing indicator
- Auto-resizing text input

## Project Structure

```
chatgpt-clone/
├── app.py              # Flask application with AI model integrations
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables file
└── templates/
    └── index.html      # Frontend HTML/CSS/JS
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- API keys for at least one of the following services (all have free tiers):
  - Google Gemini API: https://aistudio.google.com/app/apikey
  - HuggingFace API: https://huggingface.co/settings/tokens
  - OpenAI API (optional): https://platform.openai.com/api-keys

### Installation

1. Clone or download this repository

2. Navigate to the project directory:
   ```
   cd chatgpt-clone
   ```

3. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

6. Set up your environment variables:
   - Copy the `.env.example` file to `.env`
   - Add your API keys to the `.env` file
   ```
   cp .env.example .env
   # Then edit the .env file with your API keys
   ```

### Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your web browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Customization

- Add or change API keys in the `.env` file
- Add additional AI model integrations by modifying the functions in `app.py`
- Customize the UI by editing the CSS in `templates/index.html`
- Add more example prompts by editing the HTML in `templates/index.html`

## Future Enhancements

- Add user authentication
- Implement chat history storage
- Add dark mode toggle
- Add streaming responses for a more interactive experience
- Add markdown support for responses
- Implement rate limiting and usage tracking