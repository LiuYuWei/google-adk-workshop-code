# Google ADK Workshop

This repository contains projects for the Google ADK Workshop. It features four distinct agents developed using the Google Agent Development Kit (ADK).

## 🤖 Available Agents

### 1. 記帳代理人 (Accounting Agent)

The `account_agent` is a conversational AI agent designed to act as a personal accounting assistant, helping users manage their financial transactions through natural language commands.

#### ✨ Features

- **Transaction Management (CRUD):**
  - **Create:** Record new income or expenses.
  - **Read:** Query transactions by ID, category, or view all records.
  - **Update:** Modify the details of existing transactions.
  - **Delete:** Remove transactions by ID, category, or date.
- **Time-Awareness:**
  - Fetches the current time in different cities to correctly interpret time-related queries (e.g., "yesterday," "today").
- **Smart Analysis:**
  - Performs in-memory calculations to provide financial summaries, such as monthly spending by category, without needing a dedicated analysis tool.

#### 🛠️ Tools

- `add_transaction(date, description, amount, category)`
- `get_transactions(transaction_id, category)`
- `update_transaction(transaction_id, date, description, amount, category)`
- `delete_transaction(transaction_id, category, date)`
- `get_current_time(city)`

### 2. Google 部落格新聞代理人 (Google Blog News Agent)

The `google_blog_news_agent` is an agent that fetches and searches for news articles from the official Google Taiwan blog based on user-provided keywords.

#### ✨ Features

- **Keyword-Based Search:** Searches for articles on the Google Taiwan blog that match a specific keyword.
- **HTML Stripping:** Cleans up the summary content by removing HTML tags for better readability.
- **Time Queries:** Can provide the current time in any IANA timezone.

#### 🛠️ Tools

- `get_google_blog_news(keyword, max_results)`
- `get_current_time(timezone_str)`

### 3. PrivAI 內容助理 (PrivAI Context Agent)

The `privai_context_agent` is an agent that interacts with the PrivAI API to retrieve files and their content from a fileset, acting as an enterprise-level knowledge retrieval assistant.

#### ✨ Features

- **Knowledge Retrieval:** Retrieves information from PrivAI filesets based on user queries.
- **Contextual Answers:** Combines the retrieved information with the power of large language models to generate context-aware responses.

#### 🛠️ Tools

- `knowledge_rag_reference(fileset_id: str, user_query: str)`

### 4. 時區代理 (Timezone Agent)

The `timezone_agent` is a simple agent that can provide the current time in any specified IANA timezone.

#### ✨ Features

- **Time Queries:** Fetches the current time for any valid IANA timezone (e.g., 'Asia/Taipei', 'America/New_York').

#### 🛠️ Tools

- `get_current_time(timezone_str: str)`

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Access to the Google Gemini API

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/LiuYuWei/google-adk-workshop-code.git
    cd google-adk-workshop-code
    ```

2.  **Install dependencies:**
    It is recommended to create a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -r account_agent/requirements.txt
    pip install -r google_blog_news_agent/requirements.txt
    pip install -r privai_context_agent/requirements.txt
    pip install -r timezone_agent/requirements.txt
    ```

3.  **Set up your environment:**
    To set up your environment, copy the `.env.template` file to a new file named `.env` in the root directory of each agent (e.g., `account_agent/.env`, `google_blog_news_agent/.env`). Then, modify the variables in the `.env` file.

    ```bash
    cp .env.template account_agent/.env
    cp .env.template google_blog_news_agent/.env
    cp .env.template privai_context_agent/.env
    cp .env.template timezone_agent/.env
    ```

    *   **For Google Gemini API:**
        In your `.env` file, set `LITELLM_MODEL_BOOL` to `False` and provide your Google API key:
        ```
        LITELLM_MODEL_BOOL=False
        GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
        ```

    *   **For Local/LiteLLM Models:**
        In your `.env` file, set `LITELLM_MODEL_BOOL` to `True` and configure the following variables for your LiteLLM-compatible model:
        ```
        LITELLM_MODEL_BOOL=True
        LITELLM_MODEL_API_BASE="http://localhost:11434" # Example for Ollama
        LITELLM_MODEL_MODEL_NAME="ollama/llama2"      # Example for Ollama
        # LITELLM_MODEL_API_KEY is optional for many local models
        ```
        This allows you to switch between Google's models and other models like those served by Ollama or LiteLLM.

4.  **Launch the Google ADK:**
    The ADK will automatically discover the agents in the `account_agent`, `google_blog_news_agent`, `privai_context_agent`, and `timezone_agent` directories.
    ```bash
    adk web
    ```

## 📝 Usage

These agents are designed to be run within the ADK framework. Once running, you can interact with them using natural language in the ADK web interface. Select the agent you wish to interact with from the UI.

### Example Prompts

#### Accounting Agent

- **Add a transaction:**
  > "I spent 500 on dinner yesterday."

- **Query transactions:**
  > "Show me all my expenses from last week."
  > "How much did I spend on food this month?"

#### Google Blog News Agent

- **Search for news:**
  > "Find news about 'Gemini' on the Google blog."

- **Get the time:**
  > "What is the current time in 'America/New_York'?"

#### PrivAI Context Agent

- **Retrieve knowledge:**
  > "What are the data privacy regulations in the EU?" (Assuming a relevant fileset exists)

#### Timezone Agent

- **Get the time:**
  > "What time is it in 'Asia/Tokyo'?"
