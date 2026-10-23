import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


class LoginAuditStore:
    def __init__(self):
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
        self.table_name = os.environ.get("AUDIT_TABLE_NAME", "federated-login-audit")
        self.table = self.dynamodb.Table(self.table_name)

    def store_login_attempt(self, login_data: Dict[str, Any]) -> Dict[str, Any]:
        audit_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        date = datetime.now().strftime("%Y-%m-%d")

        item = {
            "audit_id": audit_id,
            "timestamp": timestamp,
            "date": date,
            "provider": login_data.get("provider", "unknown"),
            "user_id": login_data.get("user_id"),
            "status": login_data.get("status", "unknown"),
            "ip_address": login_data.get("ip_address"),
            "user_agent": login_data.get("user_agent"),
            "scope": login_data.get("scope"),
            "flow_type": login_data.get("flow_type", "oauth"),
            "error_details": json.dumps(login_data.get("error_details"))
            if login_data.get("error_details")
            else None,
            "claims_retrieved": login_data.get("claims_retrieved", False),
            "consent_granted": login_data.get("consent_granted", False),
        }

        try:
            response = self.table.put_item(Item=item)

            return {
                "success": True,
                "audit_id": audit_id,
                "timestamp": timestamp,
                "stored_data": {k: v for k, v in item.items() if v is not None},
            }

        except ClientError as e:
            return {
                "success": False,
                "error": f"DynamoDB put failed: {str(e)}",
                "audit_id": audit_id,
                "timestamp": timestamp,
            }

    def get_login_attempt(self, audit_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.table.get_item(Key={"audit_id": audit_id})
            item = response.get("Item")

            if item and "error_details" in item and item["error_details"]:
                try:
                    item["error_details"] = json.loads(item["error_details"])
                except (json.JSONDecodeError, TypeError):
                    pass

            return item

        except ClientError as e:
            print(f"Error retrieving login attempt: {e}")
            return None

    def query_logins_by_user(
        self, user_id: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        try:
            response = self.table.query(
                IndexName="user-id-index",
                KeyConditionExpression=Key("user_id").eq(user_id),
                Limit=limit,
                ScanIndexForward=False,
            )

            items = response.get("Items", [])

            for item in items:
                if "error_details" in item and item["error_details"]:
                    try:
                        item["error_details"] = json.loads(item["error_details"])
                    except (json.JSONDecodeError, TypeError):
                        pass

            return items

        except ClientError as e:
            print(f"Error querying logins by user: {e}")
            return []

    def query_logins_by_date(self, date: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            response = self.table.query(
                IndexName="date-index",
                KeyConditionExpression=Key("date").eq(date),
                Limit=limit,
                ScanIndexForward=False,
            )

            items = response.get("Items", [])

            for item in items:
                if "error_details" in item and item["error_details"]:
                    try:
                        item["error_details"] = json.loads(item["error_details"])
                    except (json.JSONDecodeError, TypeError):
                        pass

            return items

        except ClientError as e:
            print(f"Error querying logins by date: {e}")
            return []

    def query_logins_by_provider(
        self,
        provider: str,
        start_date: str = None,
        end_date: str = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        try:
            filter_expression = Key("provider").eq(provider)

            if start_date and end_date:
                filter_expression = filter_expression & Key("date").between(
                    start_date, end_date
                )

            response = self.table.scan(FilterExpression=filter_expression, Limit=limit)

            items = response.get("Items", [])

            for item in items:
                if "error_details" in item and item["error_details"]:
                    try:
                        item["error_details"] = json.loads(item["error_details"])
                    except (json.JSONDecodeError, TypeError):
                        pass

            return items

        except ClientError as e:
            print(f"Error querying logins by provider: {e}")
            return []

    def update_login_attempt(
        self, audit_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        update_expression_parts = []
        expression_attribute_names = {}
        expression_attribute_values = {}

        for key, value in updates.items():
            if value is not None:
                placeholder = f"#{key.replace('.', '_')}"
                value_placeholder = f":{key.replace('.', '_')}"

                update_expression_parts.append(f"{placeholder} = {value_placeholder}")
                expression_attribute_names[placeholder] = key
                expression_attribute_values[value_placeholder] = value

        if not update_expression_parts:
            return {"success": False, "error": "No updates provided"}

        update_expression = "SET " + ", ".join(update_expression_parts)

        try:
            response = self.table.update_item(
                Key={"audit_id": audit_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW",
            )

            updated_item = response.get("Attributes", {})

            if "error_details" in updated_item and updated_item["error_details"]:
                try:
                    updated_item["error_details"] = json.loads(
                        updated_item["error_details"]
                    )
                except (json.JSONDecodeError, TypeError):
                    pass

            return {"success": True, "audit_id": audit_id, "updated_item": updated_item}

        except ClientError as e:
            return {
                "success": False,
                "error": f"DynamoDB update failed: {str(e)}",
                "audit_id": audit_id,
            }

    def delete_login_attempt(self, audit_id: str) -> Dict[str, Any]:
        try:
            response = self.table.delete_item(
                Key={"audit_id": audit_id}, ReturnValues="ALL_OLD"
            )

            deleted_item = response.get("Attributes", {})

            return {"success": True, "audit_id": audit_id, "deleted_item": deleted_item}

        except ClientError as e:
            return {
                "success": False,
                "error": f"DynamoDB delete failed: {str(e)}",
                "audit_id": audit_id,
            }
