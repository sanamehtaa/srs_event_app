# Deployment Guide

## Setting Up API Keys

This app requires two configuration values:
- `OPENAI_API_KEY`: Your OpenAI API key
- `ASSISTANT_ID`: Your OpenAI Assistant ID

## Deployment Options

### 1. Streamlit Cloud (Recommended)

1. Go to your app's dashboard on Streamlit Cloud
2. Click on "Settings" → "Secrets"
3. Add your secrets in this format:

```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
ASSISTANT_ID = "asst-your-assistant-id-here"
```

### 2. Environment Variables

Set these environment variables before running the app:

```bash
export OPENAI_API_KEY="sk-your-openai-api-key-here"
export ASSISTANT_ID="asst-your-assistant-id-here"
```

### 3. Local Development

Create a `.streamlit/secrets.toml` file in your project root:

```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
ASSISTANT_ID = "asst-your-assistant-id-here"
```

## Getting Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create an account
3. Go to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-`)

## Getting Your Assistant ID

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to "Assistants"
3. Create a new assistant or select an existing one
4. Copy the Assistant ID (starts with `asst_`)

## Troubleshooting

- **KeyError**: Make sure your API keys are properly configured
- **Authentication Error**: Verify your OpenAI API key is valid
- **Assistant Not Found**: Ensure your Assistant ID is correct

## Security Notes

- Never commit API keys to version control
- Use environment variables or Streamlit secrets for production
- Regularly rotate your API keys 