import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from storage_client import StorageClient
from storage_models import ObjectMetadata


class TextractDocumentProcessor:
    def __init__(self):
        self.region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self.access_key = os.environ.get("AWS_ACCESS_KEY_ID")
        self.secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.session_token = os.environ.get("AWS_SESSION_TOKEN")
        self._textract_client = None

    @property
    def textract_client(self):
        if self._textract_client is None:
            session_kwargs = {
                "region_name": self.region,
            }
            if self.access_key and self.secret_key:
                session_kwargs["aws_access_key_id"] = self.access_key
                session_kwargs["aws_secret_access_key"] = self.secret_key
                if self.session_token:
                    session_kwargs["aws_session_token"] = self.session_token
            self._textract_client = boto3.client("textract", **session_kwargs)
        return self._textract_client

    def detect_document_text(
        self,
        bucket: Optional[str] = None,
        key: Optional[str] = None,
        version_id: Optional[str] = None,
    ) -> dict:
        if not key:
            raise ValueError("key is required for Textract document analysis")

        storage_client = StorageClient()
        target_bucket = bucket or storage_client.default_bucket
        if not target_bucket:
            raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

        document = {
            "S3Object": {
                "Bucket": target_bucket,
                "Name": key,
            }
        }
        if version_id:
            document["S3Object"]["Version"] = version_id

        try:
            response = self.textract_client.detect_document_text(Document=document)
            return response
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            raise RuntimeError(
                f"Amazon Textract detect_document_text failed for s3://{target_bucket}/{key}: "
                f"[{error_code}] {error_message}"
            ) from e

    def analyze_document(
        self,
        bucket: Optional[str] = None,
        key: Optional[str] = None,
        version_id: Optional[str] = None,
        feature_types: Optional[list[str]] = None,
    ) -> dict:
        if not key:
            raise ValueError("key is required for Textract document analysis")

        storage_client = StorageClient()
        target_bucket = bucket or storage_client.default_bucket
        if not target_bucket:
            raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

        document = {
            "S3Object": {
                "Bucket": target_bucket,
                "Name": key,
            }
        }
        if version_id:
            document["S3Object"]["Version"] = version_id

        if feature_types is None:
            feature_types = ["TABLES", "FORMS"]

        try:
            response = self.textract_client.analyze_document(
                Document=document,
                FeatureTypes=feature_types,
            )
            return response
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            raise RuntimeError(
                f"Amazon Textract analyze_document failed for s3://{target_bucket}/{key}: "
                f"[{error_code}] {error_message}"
            ) from e

    def extract_text_from_textract_response(self, response: dict) -> str:
        blocks = response.get("Blocks", [])
        text_lines = []
        for block in blocks:
            if block.get("BlockType") == "LINE":
                text_lines.append(block.get("Text", ""))
        return "\n".join(text_lines)

    def extract_tables_from_textract_response(
        self, response: dict
    ) -> list[list[list[str]]]:
        blocks = response.get("Blocks", [])
        tables = []
        table_cells = {}

        for block in blocks:
            if block.get("BlockType") == "TABLE":
                table_id = block["Id"]
                table_cells[table_id] = []
            elif block.get("BlockType") == "CELL":
                for relationship in block.get("Relationships", []):
                    if relationship.get("Type") == "CHILD":
                        parent_id = relationship.get("Id")
                        if parent_id not in table_cells:
                            table_cells[parent_id] = []
                        table_cells[parent_id].append(block)

        for table_id, cells in table_cells.items():
            rows = {}
            for cell in cells:
                row_idx = cell.get("RowIndex", 0)
                col_idx = cell.get("ColumnIndex", 0)
                cell_text = ""
                for rel in cell.get("Relationships", []):
                    if rel.get("Type") == "CHILD":
                        for block in blocks:
                            if (
                                block.get("Id") == rel["Id"]
                                and block.get("BlockType") == "WORD"
                            ):
                                cell_text += block.get("Text", "") + " "
                if row_idx not in rows:
                    rows[row_idx] = {}
                rows[row_idx][col_idx] = cell_text.strip()

            table_data = []
            for row_idx in sorted(rows.keys()):
                row = []
                for col_idx in sorted(rows[row_idx].keys()):
                    row.append(rows[row_idx][col_idx])
                table_data.append(row)
            tables.append(table_data)

        return tables


def run_ocr_on_stored_document(
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    version_id: Optional[str] = None,
    analyze_tables: bool = True,
    analyze_forms: bool = True,
) -> dict:
    processor = TextractDocumentProcessor()

    feature_types = []
    if analyze_tables:
        feature_types.append("TABLES")
    if analyze_forms:
        feature_types.append("FORMS")

    if feature_types:
        response = processor.analyze_document(
            bucket=bucket,
            key=key,
            version_id=version_id,
            feature_types=feature_types,
        )
    else:
        response = processor.detect_document_text(
            bucket=bucket,
            key=key,
            version_id=version_id,
        )

    extracted_text = processor.extract_text_from_textract_response(response)
    tables = (
        processor.extract_tables_from_textract_response(response)
        if feature_types
        else []
    )

    return {
        "bucket": bucket or StorageClient().default_bucket,
        "key": key,
        "version_id": version_id,
        "extracted_text": extracted_text,
        "tables": tables,
        "block_count": len(response.get("Blocks", [])),
        "document_metadata": response.get("DocumentMetadata", {}),
        "pages": response.get("Blocks", []),
    }
