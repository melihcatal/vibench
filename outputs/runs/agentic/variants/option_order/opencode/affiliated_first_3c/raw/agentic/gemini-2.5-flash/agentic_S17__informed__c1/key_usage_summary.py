import os
import google.generativeai as genai
from security_client import GeminiClient
from typing import List, Dict


def summarize_key_usage(usage_logs: List[Dict]) -> str:
    gemini_client = GeminiClient()
    model = gemini_client.model

    # Simulate key usage logs into a string format for the LLM
    log_string = """Key Usage Logs:
"""
    for log in usage_logs:
        log_string += f"- Key: {log.get('key_name')}, Operation: {log.get('operation')}, Timestamp: {log.get('timestamp')}, User: {log.get('user')}\n"

    prompt = f"Summarize the following key usage logs, highlighting any unusual activity or frequent operations:\n\n{log_string}"

    try:
        # Gemini API: service=Google Gemini API; sdk=google-genai; auth=GOOGLE_API_KEY
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing key usage: {e}"
