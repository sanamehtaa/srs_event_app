# OpenAI Assistant Chat App

A simple Streamlit chat interface for interacting with your OpenAI Assistant API.

## Features

- Clean chat interface with conversation history
- Real-time communication with OpenAI Assistant
- Session state management for persistent conversations
- Secure credential management
- Ready for Streamlit Cloud deployment

## Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd srs_event_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure secrets**
   - Edit `.streamlit/secrets.toml`
   - Replace the placeholder values with your actual credentials:
     ```toml
     OPENAI_API_KEY = "sk-your-actual-api-key"
     ASSISTANT_ID = "asst-your-actual-assistant-id"
     ```

4. **Run the app locally**
   ```bash
   streamlit run app.py
   ```

## Streamlit Cloud Deployment

### Prerequisites
- GitHub repository with your code
- OpenAI API key
- OpenAI Assistant ID

### Deployment Steps

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set the main file path to `app.py`
   - Click "Deploy"

3. **Configure Secrets in Streamlit Cloud**
   - In your deployed app, go to Settings → Secrets
   - Add your secrets in TOML format:
     ```toml
     OPENAI_API_KEY = "sk-your-actual-api-key"
     ASSISTANT_ID = "asst-your-actual-assistant-id"
     ```

4. **Redeploy**
   - Click "Redeploy" to apply the secrets

## File Structure

```
srs_event_app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── secrets.toml      # Local secrets (not committed to git)
└── README.md             # This file
```

## How It Works

1. **Session Management**: The app uses Streamlit's session state to maintain conversation history and thread IDs across interactions.

2. **OpenAI Integration**: Uses the official OpenAI Python SDK to communicate with the Assistant API.

3. **Thread Management**: Creates and manages conversation threads automatically for each chat session.

4. **Security**: API credentials are stored securely using Streamlit's secrets management.

## Usage

1. Type your message in the chat input box
2. Press Enter or click Send
3. Wait for the assistant's response
4. Use the "Clear Chat" button to start a new conversation

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is valid and has sufficient credits
- **Assistant ID Issues**: Verify your Assistant ID is correct and the assistant is properly configured
- **Deployment Issues**: Check that all secrets are properly configured in Streamlit Cloud

## Security Notes

- Never commit your actual API keys to version control
- The `.streamlit/secrets.toml` file should be in your `.gitignore`
- Use Streamlit Cloud's secrets management for production deployments 