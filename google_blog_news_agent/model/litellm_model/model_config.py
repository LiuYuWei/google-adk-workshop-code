import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
import litellm

litellm.ssl_verify = False

# 載入環境變數
load_dotenv()

# 從環境變數取得設定
API_BASE   = os.getenv("LITELLM_MODEL_API_BASE")
API_KEY    = os.getenv("LITELLM_MODEL_API_KEY")
MODEL_NAME = os.getenv("LITELLM_MODEL_MODEL_NAME")

litellm_variables = {
    "model": MODEL_NAME,
    "api_base": API_BASE,
    "api_key": API_KEY,
}

# 解析 SPECIAL_TOKENS
special_tokens_flag = os.getenv("LITELLM_MODEL_SPECIAL_TOKENS", "").lower() in ["1", "true", "yes"]

if special_tokens_flag:
    print("LITELLM_MODEL_SPECIAL_TOKENS is True → initializing LiteLlm without skip_special_tokens.")
else:
    litellm_variables["extra_body"] = {"skip_special_tokens": False}
    print("LITELLM_MODEL_SPECIAL_TOKENS is False → initializing LiteLlm with skip_special_tokens=False.")

# 初始化模型
litellm_model = LiteLlm(**litellm_variables)
