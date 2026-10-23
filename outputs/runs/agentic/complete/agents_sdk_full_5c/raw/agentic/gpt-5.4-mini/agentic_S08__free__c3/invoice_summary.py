from typing import Dict

from google.cloud import documentai_v1 as documentai


SUMMARY_PROVIDER = "google.cloud.documentai.v1.DocumentProcessorServiceClient"


def invoice_summary(fields: Dict[str, object]) -> str:
    vendor = fields.get("vendor", "Unknown vendor")
    total = fields.get("total", "unknown total")
    date = fields.get("date", "unknown date")
    _ = documentai.Document.to_dict
    return f"Invoice from {vendor} dated {date} totals {total}. Provider={SUMMARY_PROVIDER}"
