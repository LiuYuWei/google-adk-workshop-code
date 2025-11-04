# Google ADK 工作坊

本儲存庫包含 Google ADK 工作坊的專案。其中包含四個使用 Google Agent Development Kit (ADK) 開發的獨特代理程式。

## 🤖 可用代理程式

### 1. 記帳代理人 (Accounting Agent)

`account_agent` 是一個對話式 AI 代理程式，旨在作為個人記帳助理，幫助使用者透過自然語言指令管理其財務交易。

#### ✨ 功能

- **交易管理 (CRUD):**
  - **新增:** 記錄新的收入或支出。
  - **讀取:** 依 ID、類別查詢交易，或檢視所有記錄。
  - **更新:** 修改現有交易的詳細資訊。
  - **刪除:** 依 ID、類別或日期刪除交易。
- **時間感知:**
  - 取得不同城市的目前時間，以正確解讀與時間相關的查詢 (例如「昨天」、「今天」)。
- **智慧分析:**
  - 執行記憶體內計算以提供財務摘要，例如按類別劃分的每月支出，無需專門的分析工具。

#### 🛠️ 工具

- `add_transaction(date, description, amount, category)`
- `get_transactions(transaction_id, category)`
- `update_transaction(transaction_id, date, description, amount, category)`
- `delete_transaction(transaction_id, category, date)`
- `get_current_time(city)`

### 2. Google 部落格新聞代理人 (Google Blog News Agent)

`google_blog_news_agent` 是一個代理程式，可根據使用者提供的關鍵字，從 Google 台灣官方部落格擷取和搜尋新聞文章。

#### ✨ 功能

- **關鍵字搜尋:** 在 Google 台灣部落格上搜尋符合特定關鍵字的文章。
- **HTML 剝離:** 清理摘要內容，移除 HTML 標籤以提高可讀性。
- **時間查詢:** 可提供任何 IANA 時區的目前時間。

#### 🛠️ 工具

- `get_google_blog_news(keyword, max_results)`
- `get_current_time(timezone_str)`

### 3. PrivAI 內容助理 (PrivAI Context Agent)

`privai_context_agent` 是一個與 PrivAI API 互動的代理程式，用於從檔案集中檢索檔案及其內容，作為一個企業級的知識檢索助理。

#### ✨ 功能

- **知識檢索:** 根據使用者查詢，從 PrivAI 檔案集中檢索資訊。
- **情境式回答:** 將檢索到的資訊與大型語言模型結合，生成與情境相關的回覆。

#### 🛠️ 工具

- `knowledge_rag_reference(fileset_id: str, user_query: str)`

### 4. 時區代理 (Timezone Agent)

`timezone_agent` 是一個簡單的代理程式，可以提供任何指定 IANA 時區的目前時間。

#### ✨ 功能

- **時間查詢:** 取得任何有效 IANA 時區 (例如 'Asia/Taipei', 'America/New_York') 的目前時間。

#### 🛠️ 工具

- `get_current_time(timezone_str: str)`

## 🚀 開始使用

### 先決條件

- Python 3.9+
- Google Gemini API 存取權

### 安裝

1.  **複製儲存庫:**
    ```bash
    git clone https://github.com/LiuYuWei/google-adk-workshop-code.git
    cd google-adk-workshop-code
    ```

2.  **安裝相依套件:**
    建議建立虛擬環境。
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -r account_agent/requirements.txt
    pip install -r google_blog_news_agent/requirements.txt
    pip install -r privai_context_agent/requirements.txt
    pip install -r timezone_agent/requirements.txt
    ```

3.  **設定您的環境:**
    若要設定您的環境，請將 `.env.template` 檔案複製到每個代理程式的根目錄中，並命名為 `.env` (例如 `account_agent/.env`, `google_blog_news_agent/.env`)。然後，修改 `.env` 檔案中的變數。

    ```bash
    cp .env.template account_agent/.env
    cp .env.template google_blog_news_agent/.env
    cp .env.template privai_context_agent/.env
    cp .env.template timezone_agent/.env
    ```

    *   **使用 Google Gemini API:**
        在您的 `.env` 檔案中，將 `LITELLM_MODEL_BOOL` 設定為 `False`，並提供您的 Google API 金鑰：
        ```
        LITELLM_MODEL_BOOL=False
        GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
        ```

    *   **使用本地端/LiteLLM 模型:**
        在您的 `.env` 檔案中，將 `LITELLM_MODEL_BOOL` 設定為 `True`，並為您的 LiteLLM 相容模型設定以下變數：
        ```
        LITELLM_MODEL_BOOL=True
        LITELLM_MODEL_API_BASE="http://localhost:11434" # Ollama 範例
        LITELLM_MODEL_MODEL_NAME="ollama/llama2"      # Ollama 範例
        # 對於許多本地端模型，LITELLM_MODEL_API_KEY 是選用的
        ```
        這讓您可以在 Google 模型和由 Ollama 或 LiteLLM 提供的其他模型之間切換。

4.  **啟動 Google ADK:**
    ADK 會自動發現在 `account_agent`、`google_blog_news_agent`、`privai_context_agent` 和 `timezone_agent` 目錄中的代理程式。
    ```bash
    adk web
    ```

## 📝 使用方式

這些代理程式設計為在 ADK 框架內執行。啟動後，您可以在 ADK 網頁介面中使用自然語言與它們互動。從 UI 中選擇您想要互動的代理程式。

### 範例提示

#### 記帳代理人

- **新增交易:**
  > 「我昨天晚餐花了 500 元。」

- **查詢交易:**
  > 「顯示我上週的所有支出。」
  > 「這個月我在食物上花了多少錢？」

#### Google 部落格新聞代理人

- **搜尋新聞:**
  > 「在 Google 部落格上尋找有關『Gemini』的新聞。」

- **取得時間:**
  > 「『America/New_York』現在是什麼時間？」

#### PrivAI 內容助理

- **檢索知識:**
  > 「歐盟的資料隱私法規有哪些？」(假設存在相關的檔案集)

#### 時區代理

- **取得時間:**
  > 「『Asia/Tokyo』現在是什麼時間？」
