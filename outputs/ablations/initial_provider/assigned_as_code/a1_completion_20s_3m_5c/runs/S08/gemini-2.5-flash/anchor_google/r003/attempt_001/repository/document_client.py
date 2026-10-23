import os
import json

class DocumentClientConfig:
    def __init__(self):
        self.google_project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.google_location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
        self.document_ai_invoice_processor_id = os.getenv("DOCUMENT_AI_INVOICE_PROCESSOR_ID")
        self.document_ai_receipt_processor_id = os.getenv("DOCUMENT_AI_RECEIPT_PROCESSOR_ID")
        
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.aws_glue_schema_name = os.getenv("AWS_GLUE_SCHEMA_NAME", "expense_schema")
        self.aws_glue_registry_name = os.getenv("AWS_GLUE_REGISTRY_NAME", "default-registry")
        self.aws_comprehend_min_confidence = float(os.getenv("AWS_COMPREHEND_MIN_CONFIDENCE", "0.7"))

        self.vertex_ai_project_id = os.getenv("VERTEX_AI_PROJECT_ID")
        self.vertex_ai_location = os.getenv("VERTEX_AI_LOCATION", "us-central1")
        self.vertex_ai_text_model = os.getenv("VERTEX_AI_TEXT_MODEL", "gemini-pro")

        self.google_nl_project_id = os.getenv("GOOGLE_NL_PROJECT_ID")
        self.google_nl_location = os.getenv("GOOGLE_NL_LOCATION", "global")

        self.google_translate_project_id = os.getenv("GOOGLE_TRANSLATE_PROJECT_ID")
        self.google_translate_location = os.getenv("GOOGLE_TRANSLATE_LOCATION", "global")

        self.firestore_project_id = os.getenv("FIRESTORE_PROJECT_ID")
        self.firestore_collection_name = os.getenv("FIRESTORE_COLLECTION_NAME", "expense_records")

    def get_document_ai_invoice_config(self):
        return {
            "project_id": self.google_project_id,
            "location": self.google_location,
            "processor_id": self.document_ai_invoice_processor_id
        }

    def get_document_ai_receipt_config(self):
        return {
            "project_id": self.google_project_id,
            "location": self.google_location,
            "processor_id": self.document_ai_receipt_processor_id
        }

    def get_aws_glue_schema_config(self):
        return {
            "aws_region": self.aws_region,
            "schema_name": self.aws_glue_schema_name,
            "registry_name": self.aws_glue_registry_name
        }

    def get_aws_comprehend_config(self):
        return {
            "aws_region": self.aws_region,
            "min_confidence": self.aws_comprehend_min_confidence
        }

    def get_vertex_ai_config(self):
        return {
            "project_id": self.vertex_ai_project_id,
            "location": self.vertex_ai_location,
            "model_name": self.vertex_ai_text_model
        }

    def get_google_nl_config(self):
        return {
            "project_id": self.google_nl_project_id,
            "location": self.google_nl_location
        }

    def get_google_translate_config(self):
        return {
            "project_id": self.google_translate_project_id,
            "location": self.google_translate_location
        }

    def get_firestore_config(self):
        return {
            "project_id": self.firestore_project_id,
            "collection_name": self.firestore_collection_name
        }

# Example usage (not part of the class, but for context)
# config = DocumentClientConfig()
# invoice_config = config.get_document_ai_invoice_config()
# receipt_config = config.get_document_ai_receipt_config()
