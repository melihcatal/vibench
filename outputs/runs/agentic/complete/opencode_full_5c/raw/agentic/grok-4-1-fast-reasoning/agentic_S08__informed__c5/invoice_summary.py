import os
import json
import google.generativeai as genai
from document_models import NormalizedExpense


def invoice_summary(normalized_expense: NormalizedExpense) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    data_str = json.dumps(normalized_expense.model_dump(), default=str, indent=2)
    prompt = f"""Provide a concise 2-3 sentence summary of this invoice:
{data_str}"""
    response = model.generate_content(prompt)
    return response.text
