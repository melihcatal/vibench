import os
import google.generativeai as genai
from document_models import NormalizedExpense

def summarize_invoice(expense: NormalizedExpense) -> str:
    gemini_api_key = os.environ.get("GOOGLE_API_KEY")
    if not gemini_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=gemini_api_key)

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
Summarize the following expense record into a concise sentence or two, highlighting the vendor, total amount, and a brief description.

Vendor: {expense.vendor}
Date: {expense.date}
Amount: {expense.amount} {expense.currency}
Description: {expense.description}
Line Items: {', '.join([f'{item.description} ({item.amount} {expense.currency})' for item in expense.line_items])}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary with Gemini API: {e}")
        return "Could not generate summary."

if __name__ == '__main__':
    # Example usage:
    # from document_models import NormalizedExpense, LineItem
    # expense_data = NormalizedExpense(
    #     vendor="Global Tech Solutions",
    #     date="2023-11-15",
    #     amount=2500.50,
    #     currency="USD",
    #     description="Consulting services for Q4 project.",
    #     line_items=[
    #         LineItem(description="Consulting Hours", amount=2000.0),
    #         LineItem(description="Software Licenses", amount=500.50)
    #     ]
    # )
    # summary = summarize_invoice(expense_data)
    # print("Summary:", summary)
    pass
