import os
import json
import requests
from urllib.parse import urlencode

def knowledge_rag_reference(fileset_id: str, user_query: str) -> str:
    """
    呼叫 PrivAI RAG API 進行檔案檢索。
    :param fileset_id: 已上傳檔案集合的 ID
    :param prompt_id: (未使用)
    :param user_query: 使用者查詢字串
    :param model_name: (未使用)
    :return: 檢索到的文件內容
    """
    base_url = "{}v1/chat/references".format(os.getenv("PRIVAI_API_URL"))
    params = {
        "fileset_id": fileset_id,
        "query": user_query
    }
    url = f"{base_url}?{urlencode(params)}"
    
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + os.getenv("PRIVAI_API_KEY")
    }

    response = requests.post(url, headers=headers, data="", verify=True)

    if response.status_code == 200:
        result = response.json()
        return json.dumps(result, indent=2, ensure_ascii=False)
    else:
        raise {"Content": "PrivAI API 呼叫失敗", "status_code": response.status_code, "response": response.text}
