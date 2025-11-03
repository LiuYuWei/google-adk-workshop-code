import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from google.adk.agents import Agent
import requests
import feedparser
import re
from typing import List, Dict, Union
from .model.litellm_model.model_config import litellm_model


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

# 保持您的 Agent 定義不變
root_agent = Agent(
    name="time_agent",
    model=litellm_model,
    description=(
        "Agent to answer questions about the time in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time in a city. "
        "You will be given a timezone string to find the current time."
    ),
    tools=[get_current_time],
)
