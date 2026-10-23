import os

import requests


def profile_note_store(document: dict):
    response = requests.post("https://api.notion.com/v1/pages", headers={"Authorization": f"Bearer {os.getenv('NOTION_API_KEY', '')}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}, json=document, timeout=30)
    response.raise_for_status()
    return response.json()
