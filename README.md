# Google ADK Workshop

This repository contains projects for the Google ADK Workshop. It features two distinct agents developed using the Google Agent Development Kit (ADK).

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

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Access to the Google Gemini API

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/LiuYuWei/agentic-ai-developer-day-2025-adk-workshop.git
    cd agentic-ai-developer-day-2025-adk-workshop
    ```

2.  **Install dependencies:**
    It is recommended to create a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -r account_agent/requirements.txt
    pip install -r google_blog_news_agent/requirements.txt
    ```

3.  **Set up your environment:**
    You will need to configure your environment with the necessary credentials for the Gemini API.

4.  **Launch the Google ADK:**
    The ADK will automatically discover the agents in the `account_agent` and `google_blog_news_agent` directories.
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
