import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_privai_files_from_privai_fileset(fileset_id: str) -> list[dict[str, str]]:
    """
    Retrieves a list of files from a given PrivAI fileset ID.

    Args:
        fileset_id: The ID of the PrivAI fileset to retrieve files from.

    Returns:
        A list of dictionaries, where each dictionary contains the
        'filename' and 'id' of a file from the PrivAI fileset.
    """
    api_url = os.getenv("PRIVAI_API_URL")
    api_key = os.getenv("PRIVAI_API_KEY")
    
    if not api_url or not api_key:
        raise ValueError("PRIVAI_API_URL and PRIVAI_API_KEY must be set in the .env file")

    url = f"{api_url}v1/filesets/{fileset_id}/files?limit=10000&order=desc&files_state=completed"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return [{"filename": file["filename"], "id": file["id"], "used_quality": file["used_quality"]} for file in data.get("data", [])]

def get_privai_file_context(file_id: str, quality: str) -> str:
    """
    Retrieves the content of a file from PrivAI.

    Args:
        file_id: The ID of the file to retrieve from PrivAI.
        quality: The quality of the file to retrieve (e.g., STD, LQ, HQ).

    Returns:
        The content of the file as a string.
    """
    api_url = os.getenv("PRIVAI_API_URL")
    api_key = os.getenv("PRIVAI_API_KEY")

    if not api_url or not api_key:
        raise ValueError("PRIVAI_API_URL and PRIVAI_API_KEY must be set in the .env file")

    url = f"{api_url}v1/files/{file_id}/content?file_type=parsed_result&quality={quality}"
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text
