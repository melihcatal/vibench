import os
from google.generativeai import GenerativeModel

model = GenerativeModel('gemini-1.5-pro-latest')

def summarize_invoice(invoice_data):
    response = model.generate_content(f'Summarize the following invoice: {invoice_data}')
    return response.text