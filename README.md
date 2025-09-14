# Agentic AI 開發者日 2025 - ADK 工作坊

這個儲存庫包含了 Agentic AI 開發者日 2025 台北 ADK 工作坊的專案。

## 🤖 記帳代理人 (Account Agent)

`account_agent` 是ㄧ個使用 Google Agent Development Kit (ADK) 開發的對話式 AI 代理人。它扮演著個人記帳助理的角色，幫助使用者透過自然語言指令來管理他們的財務交易。

### ✨ 功能

- **交易管理 (CRUD):**
  - **新增:** 記錄新的收入或支出。
  - **查詢:** 依據 ID、類別查詢交易，或檢視所有記錄。
  - **更新:** 修改現有交易的詳細資訊。
  - **刪除:** 依據 ID、類別或日期刪除交易。
- **時間感知:**
  - 獲取不同城市的目前時間，以正確解讀與時間相關的查詢 (例如：「昨天」、「今天」)。
- **智慧分析:**
  - 執行記憶體內計算以提供財務摘要，例如按類別分的每月支出，無需專用的分析工具。

### 🛠️ 技術棧

- **框架:** Google Agent Development Kit (ADK)
- **語言:** Python
- **資料庫:** SQLite

### 🚀 開始使用

#### 先決條件

- Python 3.9+
- Google Gemini API 的存取權限

#### 安裝

1.  **複製儲存庫:**
    ```bash
    git clone https://github.com/LiuYuWei/agentic-ai-developer-day-2025-adk-workshop.git
    cd agentic-ai-developer-day-2025-adk-workshop
    ```

2.  **安裝相依套件:**
    建議建立一個虛擬環境。
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install google-adk
    ```

3.  **設定您的環境:**
    您將需要使用 Gemini API 的必要憑證來設定您的環境。

4.  **啟動 Google ADK:**
    ```bash
    adk web
    ```

### 📝 使用方式

此代理人設計為在 ADK 框架內執行。一旦執行，您就可以使用自然語言與它互動。

**範例提示:**

- **新增交易:**
  > 「我昨天晚餐花了 500 元。」

- **查詢交易:**
  > 「顯示我上週的所有支出。」
  > 「這個月我在食物上花了多少錢？」

- **刪除交易:**
  > 「刪除我今天午餐的交易。」

- **財務分析:**
  > 「這個月我的總支出是多少？」
  > 「六月份我在哪個類別上花最多錢？」
