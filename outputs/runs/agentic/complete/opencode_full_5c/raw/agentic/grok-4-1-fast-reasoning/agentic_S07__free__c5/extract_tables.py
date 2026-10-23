import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from document_models import TablesResponse

endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)


def extract_tables(image_path: str) -> TablesResponse:
    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout", analyze_request=f, content_type="image/jpeg"
        )
    result: AnalyzeResult = poller.result()
    tables = []
    for table in result.tables:
        rows = [
            [cell.content for cell in row_span.cells] for row_span in table.row_span
        ]
        tables.append({"rows": rows})
    return {"tables": tables}
