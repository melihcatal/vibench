import os
from typing import Dict, Any
from document_client import DocumentAIClient
from document_models import NormalizedExpense
import google.generativeai as genai

def summarize_invoice_fields(expense_data: NormalizedExpense) -> Dict[str, Any]:
    model = DocumentAIClient().get_gemini_client()

    prompt = f"""Summarize the following expense record into a concise paragraph. Focus on the vendor, total amount, date, and a brief mention of line items if available. If a note is present, include it. 

Expense Record (JSON): {expense_data.to_dict()}

Summary:"""

    try:
        response = model.generate_content(prompt)
        summary_text = response.text
        return {"success": True, "summary": summary_text}
    except Exception as e:
        return {"success": False, "error": str(e)}
