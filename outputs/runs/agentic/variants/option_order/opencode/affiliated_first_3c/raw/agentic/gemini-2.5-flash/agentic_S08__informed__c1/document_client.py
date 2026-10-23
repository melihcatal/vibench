import os
from google.cloud import documentai_v1beta3 as documentai
from google.generativeai.client import get_default_retriever_async_client
import google.generativeai as genai
from google.cloud import translate_v2 as translate
from google.cloud import firestore
import boto3
import requests


class DocumentClient:
    def __init__(self):
        # Google Document AI Client (for extract_invoice_fields.py)
        self.documentai_client = documentai.DocumentProcessorServiceClient()
        self.documentai_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.documentai_location = "us"
        self.documentai_invoice_processor_id = os.environ.get(
            "DOCUMENT_AI_INVOICE_PROCESSOR_ID"
        )

        # Amazon Textract Client (for extract_receipt_fields.py)
        self.textract_client = boto3.client(
            "textract", region_name=os.environ.get("AWS_REGION", "us-east-1")
        )

        # Google Gemini API Client (for invoice_summary.py)
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.gemini_model = genai.GenerativeModel("gemini-pro")

        # Perspective API (for vendor_text_safety.py)
        self.perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
        self.perspective_api_endpoint = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

        # Google Cloud Translation Client (for invoice_note_translate.py)
        self.translate_client = translate.Client()

        # Google Firestore Client (for expense_record_store.py)
        self.firestore_client = firestore.Client()
        self.firestore_collection_name = "expense_records"

    def get_documentai_processor_path(self, processor_id: str):
        return self.documentai_client.processor_path(
            self.documentai_project_id, self.documentai_location, processor_id
        )
