import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from google.adk.agents import Agent
import requests
import feedparser
import re
from typing import List, Dict, Union


def get_current_time(timezone_str: str) -> dict:
    """Returns the current time in a specified IANA timezone.

    Args:
        timezone_str: The IANA timezone name (e.g., 'Asia/Taipei', 'America/New_York').

    Returns:
        dict: A dictionary with the status and the result or an error message.
    """
    try:
        # 使用 ZoneInfo 獲取指定時區的資訊
        tz = ZoneInfo(timezone_str)
        # 獲取該時區的當前時間
        current_time = datetime.datetime.now(tz)
        # 將時間格式化為易於閱讀的字串
        time_report = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        report = f"The current time in {timezone_str} is {time_report}."
        # 返回成功的結果
        return {"status": "success", "report": report}
    except ZoneInfoNotFoundError:
        # 如果找不到時區，返回錯誤訊息
        error_msg = f"Error: Timezone '{timezone_str}' not found. Please use a valid IANA timezone name."
        return {"status": "error", "report": error_msg}
    except Exception as e:
        # 處理其他潛在的錯誤
        error_msg = f"An unexpected error occurred: {e}"
        return {"status": "error", "report": error_msg}


def strip_html_tags(html: str) -> str:
    """
    移除 HTML 標籤，保留段落換行
    """
    # 直接使用正規表達式清理 HTML 標籤
    return re.sub(r'<[^>]*>', '', html).strip()


def get_google_blog_news(
    keyword: str,
    max_results: int = 1
) -> Dict[str, Union[str, List[Dict[str, str]]]]:
    """
    僅使用 feedparser 從 Google 台灣官方部落格 RSS 提取新聞，根據關鍵字搜尋並回傳前 N 筆結果。

    Args:
        keyword (str): 要搜尋的關鍵字（不區分大小寫）
        max_results (int): 最多回傳新聞數量，預設為 1

    Returns:
        dict: 包含 status 及 reports 或 error_message
    """
    feed_url = "https://blog.google/intl/zh-tw/rss/"
    try:
        # 解析 RSS Feed（feedparser 會自動發送請求）
        feed = feedparser.parse(feed_url)
        # 檢查 feed 解析是否有錯誤
        if feed.bozo:
            raise feed.bozo_exception

        # 編譯關鍵字正則表達式
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        results: List[Dict[str, str]] = []

        for entry in feed.entries:
            title = entry.get('title', '')
            summary_html = entry.get('summary', '')
            combined_text = f"{title} {summary_html}"

            if pattern.search(combined_text):
                # 清理 HTML 標籤
                summary_text = strip_html_tags(summary_html)
                results.append({
                    'title': title,
                    'link': entry.get('link', ''),
                    'summary': summary_text,
                    'pubDate': entry.get('published', '')
                })
                if len(results) >= max_results:
                    break

        if not results:
            return {
                'status': 'error',
                'error_message': f"未找到關鍵字「{keyword}」的相關新聞。"
            }

        return {'status': 'success', 'reports': results}

    except Exception as e:
        # 任何解析或請求過程中出錯，都回傳錯誤訊息
        return {
            'status': 'error',
            'error_message': f"處理 RSS Feed 時發生錯誤: {e}"
        }

# 保持您的 Agent 定義不變
root_agent = Agent(
    name="time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time in a city. "
        "You will be given a timezone string to find the current time."
    ),
    tools=[get_current_time, get_google_blog_news],
)
