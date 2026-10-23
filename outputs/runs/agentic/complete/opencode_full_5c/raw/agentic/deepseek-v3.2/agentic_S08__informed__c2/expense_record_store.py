import os
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import uuid
from document_models import ExpenseRecord


class ExpenseRecordStore:
    """Persist normalized expense records in Amazon DynamoDB."""

    def __init__(self, table_name: str = None, region_name: str = None):
        """Initialize DynamoDB client and table."""
        self.table_name = table_name or os.getenv(
            "DYNAMODB_TABLE_NAME", "expense-records"
        )
        self.region_name = region_name or os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=self.region_name,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

        self.table = self.dynamodb.Table(self.table_name)

    def store_expense_record(self, expense_record: ExpenseRecord) -> Dict[str, Any]:
        """
        Store an expense record in DynamoDB.

        Args:
            expense_record: ExpenseRecord object

        Returns:
            Dictionary with storage result
        """
        record_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        item = {
            "record_id": record_id,
            "document_type": expense_record.document_type,
            "vendor": expense_record.vendor,
            "date": expense_record.date,
            "total": str(expense_record.total),
            "currency": expense_record.currency,
            "line_items": expense_record.line_items,
            "metadata": expense_record.metadata,
            "extracted_at": expense_record.extracted_at,
            "confidence": str(expense_record.confidence),
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        try:
            response = self.table.put_item(Item=item)

            return {
                "success": True,
                "record_id": record_id,
                "item": item,
                "response_metadata": response.get("ResponseMetadata", {}),
            }

        except ClientError as e:
            raise Exception(f"Failed to store expense record in Amazon DynamoDB: {e}")

    def get_expense_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an expense record by ID.

        Args:
            record_id: Record ID

        Returns:
            Expense record dictionary or None
        """
        try:
            response = self.table.get_item(Key={"record_id": record_id})
            return response.get("Item")
        except ClientError as e:
            raise Exception(f"Failed to get expense record from Amazon DynamoDB: {e}")

    def query_by_vendor(self, vendor: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Query expense records by vendor.

        Args:
            vendor: Vendor name
            limit: Maximum number of records to return

        Returns:
            List of expense records
        """
        try:
            response = self.table.query(
                IndexName="vendor-index",
                KeyConditionExpression="vendor = :v",
                ExpressionAttributeValues={":v": vendor},
                Limit=limit,
            )
            return response.get("Items", [])
        except ClientError:
            try:
                response = self.table.scan(
                    FilterExpression="vendor = :v",
                    ExpressionAttributeValues={":v": vendor},
                    Limit=limit,
                )
                return response.get("Items", [])
            except ClientError as e:
                raise Exception(
                    f"Failed to query expense records by vendor from Amazon DynamoDB: {e}"
                )

    def query_by_date_range(
        self, start_date: str, end_date: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Query expense records by date range.

        Args:
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            limit: Maximum number of records to return

        Returns:
            List of expense records
        """
        try:
            response = self.table.scan(
                FilterExpression="#d between :start and :end",
                ExpressionAttributeNames={"#d": "date"},
                ExpressionAttributeValues={":start": start_date, ":end": end_date},
                Limit=limit,
            )
            return response.get("Items", [])
        except ClientError as e:
            raise Exception(
                f"Failed to query expense records by date range from Amazon DynamoDB: {e}"
            )

    def update_expense_record(
        self, record_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an expense record.

        Args:
            record_id: Record ID
            updates: Dictionary of fields to update

        Returns:
            Dictionary with update result
        """
        update_expression_parts = []
        expression_attribute_values = {}
        expression_attribute_names = {}

        for i, (key, value) in enumerate(updates.items()):
            if key == "record_id":
                continue

            placeholder = f":val{i}"
            name_placeholder = f"#attr{i}"

            update_expression_parts.append(f"{name_placeholder} = {placeholder}")
            expression_attribute_values[placeholder] = value
            expression_attribute_names[name_placeholder] = key

        update_expression_parts.append("#updated = :now")
        expression_attribute_names["#updated"] = "updated_at"
        expression_attribute_values[":now"] = datetime.utcnow().isoformat()

        update_expression = "SET " + ", ".join(update_expression_parts)

        try:
            response = self.table.update_item(
                Key={"record_id": record_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW",
            )

            return {
                "success": True,
                "updated_item": response.get("Attributes", {}),
                "response_metadata": response.get("ResponseMetadata", {}),
            }

        except ClientError as e:
            raise Exception(f"Failed to update expense record in Amazon DynamoDB: {e}")

    def delete_expense_record(self, record_id: str) -> Dict[str, Any]:
        """
        Delete an expense record.

        Args:
            record_id: Record ID

        Returns:
            Dictionary with deletion result
        """
        try:
            response = self.table.delete_item(Key={"record_id": record_id})

            return {
                "success": True,
                "record_id": record_id,
                "response_metadata": response.get("ResponseMetadata", {}),
            }

        except ClientError as e:
            raise Exception(
                f"Failed to delete expense record from Amazon DynamoDB: {e}"
            )

    def batch_store_records(
        self, expense_records: List[ExpenseRecord]
    ) -> List[Dict[str, Any]]:
        """
        Batch store multiple expense records.

        Args:
            expense_records: List of ExpenseRecord objects

        Returns:
            List of storage results
        """
        results = []

        with self.table.batch_writer() as batch:
            for expense_record in expense_records:
                record_id = str(uuid.uuid4())
                timestamp = datetime.utcnow().isoformat()

                item = {
                    "record_id": record_id,
                    "document_type": expense_record.document_type,
                    "vendor": expense_record.vendor,
                    "date": expense_record.date,
                    "total": str(expense_record.total),
                    "currency": expense_record.currency,
                    "line_items": expense_record.line_items,
                    "metadata": expense_record.metadata,
                    "extracted_at": expense_record.extracted_at,
                    "confidence": str(expense_record.confidence),
                    "created_at": timestamp,
                    "updated_at": timestamp,
                }

                try:
                    batch.put_item(Item=item)
                    results.append(
                        {
                            "success": True,
                            "record_id": record_id,
                            "vendor": expense_record.vendor,
                        }
                    )
                except ClientError as e:
                    results.append(
                        {
                            "success": False,
                            "error": str(e),
                            "vendor": expense_record.vendor,
                        }
                    )

        return results
