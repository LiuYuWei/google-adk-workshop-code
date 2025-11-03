import sqlite3
from typing import Optional
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from .model.litellm_model.model_config import litellm_model

# Initialize the database
def init_db():
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         date TEXT NOT NULL,
         description TEXT NOT NULL,
         amount REAL NOT NULL,
         category TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

init_db()

def add_transaction(date: str, description: str, amount: float, category: str) -> dict:
    """Adds a new transaction record to the database."""
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (date, description, amount, category) VALUES (?, ?, ?, ?)",
              (date, description, amount, category))
    transaction_id = c.lastrowid
    conn.commit()
    conn.close()
    return {"status": "success", "report": f"Transaction record created with ID: {transaction_id}"}

def get_transactions(transaction_id: Optional[int] = None, category: Optional[str] = None) -> dict:
    """Retrieves all transaction records, or filtered by ID or category from the database."""
    conn = sqlite3.connect('accounting.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if transaction_id:
        c.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        transaction = c.fetchone()
        conn.close()
        if transaction:
            return {"status": "success", "report": dict(transaction)}
        else:
            return {"status": "error", "error_message": f"Transaction with ID {transaction_id} not found."}
    elif category:
        c.execute("SELECT * FROM transactions WHERE category = ?", (category,))
        transactions = c.fetchall()
        conn.close()
        return {"status": "success", "report": [dict(row) for row in transactions]}
    else:
        c.execute("SELECT * FROM transactions")
        transactions = c.fetchall()
        conn.close()
        return {"status": "success", "report": [dict(row) for row in transactions]}

def update_transaction(transaction_id: int, date: Optional[str] = None, description: Optional[str] = None, amount: Optional[float] = None, category: Optional[str] = None) -> dict:
    """Updates an existing transaction record in the database."""
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    
    updates = []
    params = []
    if date:
        updates.append("date = ?")
        params.append(date)
    if description:
        updates.append("description = ?")
        params.append(description)
    if amount:
        updates.append("amount = ?")
        params.append(amount)
    if category:
        updates.append("category = ?")
        params.append(category)

    if not updates:
        conn.close()
        return {"status": "error", "error_message": "No fields to update."}

    params.append(transaction_id)
    c.execute(f"UPDATE transactions SET { ', '.join(updates)} WHERE id = ?", tuple(params))
    
    conn.commit()
    
    if c.rowcount == 0:
        conn.close()
        return {"status": "error", "error_message": f"Transaction with ID {transaction_id} not found."}
    else:
        conn.close()
        return {"status": "success", "report": f"Transaction with ID {transaction_id} updated."}

def delete_transaction(transaction_id: Optional[int] = None, category: Optional[str] = None, date: Optional[str] = None) -> dict:
    """Deletes transaction records from the database based on ID, category, or date.

    Args:
        transaction_id (Optional[int], optional): The ID of the transaction to delete. Defaults to None.
        category (Optional[str], optional): The category of transactions to delete. Defaults to None.
        date (Optional[str], optional): The date of transactions to delete (YYYY-MM-DD). Defaults to None.

    Returns:
        dict: status and result or error msg.
    """
    if not transaction_id and not category and not date:
        return {
            "status": "error",
            "error_message": "You must provide at least one criterion (ID, category, or date) for deletion."
        }

    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    
    where_clauses = []
    params = []
    
    if transaction_id:
        where_clauses.append("id = ?")
        params.append(transaction_id)
    if category:
        where_clauses.append("category = ?")
        params.append(category)
    if date:
        where_clauses.append("date = ?")
        params.append(date)
        
    where_sql = " AND ".join(where_clauses)
    
    query = f"DELETE FROM transactions WHERE {where_sql}"
    
    c.execute(query, tuple(params))
    
    deleted_rows = c.rowcount
    conn.commit()
    conn.close()
    
    if deleted_rows > 0:
        return {"status": "success", "report": f"Successfully deleted {deleted_rows} transaction(s)."}
    else:
        return {"status": "error", "error_message": "No matching transactions found to delete."}

def get_current_time(city: str = "Taipei") -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time. Defaults to "Taipei".

    Returns:
        dict: status and result or error msg.
    """

    # A simple mapping from city to timezone identifier
    timezone_map = {
        "new york": "America/New_York",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
        "sydney": "Australia/Sydney",
        "taipei": "Asia/Taipei",
    }
    
    tz_identifier = timezone_map.get(city.lower())

    if not tz_identifier:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

root_agent = Agent(
    name="accounting_agent",
    model=litellm_model,
    description=(
        "Agent for accounting, primarily for users in Taiwan. It can get the current time and manage transactions."
    ),
    instruction=(
        """你是一位頂尖的 AI 記帳助理，專為台灣使用者設計，目標是提供**快速**且**安全**的服務。請嚴格遵循以下工作流程：

**最高指導原則：時間基準**
在你執行任何有關交易紀錄的任務（新增、查詢、更新、刪除）之前，如果使用者的指令中**包含了任何與時間相關的詞彙**（例如「今天」、「昨天」、「上禮拜」、「星期三」等），你的**第一個動作**必須是呼叫 `get_current_time` 來獲取一個準確的「今天」作為後續所有日期計算的基準。

**A. 新增 (Create)**
1.  **智慧判斷**：根據上述原則獲取時間基準後，你必須自動完成以下兩件事：
    *   **日期**：將相對日期（如「昨天」）轉換為 `YYYY-MM-DD` 格式。
    *   **分類**：根據描述推斷出最合理的分類。
2.  **主動執行**：一旦獲取了完整的交易資訊，立即呼叫 `add_transaction`，無需再次詢問。

**B. 查詢 (Read)**
1.  **清晰回覆**：根據時間基準計算出正確的查詢日期後，使用 `get_transactions` 查詢資料並清晰地回覆。

**C. 更新 (Update)**
1.  **精準定位**：根據時間基準計算出目標日期後，你必須先找到使用者想修改的**單一紀錄的 ID**。
2.  **確認目標**：最好和使用者確認目標紀錄（例如「您是指 ID 為 5，昨天關於『買晚餐』的這筆紀錄嗎？」），然後再呼叫 `update_transaction`。

**D. 刪除 (Delete)**
1.  **安全第一**：刪除是無法復原的。
2.  **批量刪除確認**：如果使用者要求根據「日期」或「類別」刪除，你必須：
    a. 根據時間基準計算出目標日期。
    b. 用 `get_transactions` 查詢將被影響的紀錄有幾筆。
    c. 向使用者回報筆數並請求最終確認後，才能呼叫 `delete_transaction`。

**E. 智慧分析 (Analysis)**
你本身就具備強大的資料分析能力。當使用者提出分析請求時（例如「上個月花最多錢在哪？」或「結算本月收支」），你**不需**尋找特定的分析工具，而是應該遵循以下步驟：

1.  **確定範圍 (Determine Scope)**：根據使用者的問題，確定分析的**時間範圍**和**目標**（例如，是想知道總和，還是按類別分組）。
2.  **獲取原始數據 (Fetch Raw Data)**：呼叫 `get_transactions` 工具，以獲取所有相關的交易紀錄。
3.  **在心中進行運算 (Perform In-Memory Calculation)**：`get_transactions` 會回傳一個包含多筆交易紀錄的列表。你需要在你的思考過程中，遍歷這個列表並進行計算：
    *   **計算總收支**：初始化 `總收入` 和 `總支出` 為 0。遍歷每一筆紀錄，如果 `amount` 是正數，就加到 `總收入`；如果是負數，就加到 `總支出`。
    *   **按類別分組**：建立一個字典（dictionary）來存放每個類別的總支出。遍歷每一筆紀錄，將支出金額累加到對應類別的鍵（key）中。
    *   **找出最大值**：在按類別分組後，找出字典中值最大的那個類別。
4.  **呈現分析結果 (Present the Result)**：將你計算出的結果，用清晰、有條理的方式呈現給使用者。

**F. 通用規則**
1.  **預設值**：貨幣為「新台幣 (TWD)」，時間查詢的地區為「台北」。
2.  **核心功能**：你的任務是管理記帳（CRUD）、分析資料與時間查詢。"""
    ),
    tools=[add_transaction, get_transactions, update_transaction, delete_transaction, get_current_time],
)