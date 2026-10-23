import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def summarize_key_usage(events: list[str]) -> str:
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""Summarize the following key usage and cryptographic events into a concise report:

{"\n".join(events)}

Summary:"""
    response = model.generate_content(prompt)
    return response.text
