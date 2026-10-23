import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError


class LoginAuditStore:
    """Persist federated-login audit records in Azure Cosmos DB."""

    def __init__(self):
        endpoint = os.environ.get("AZURE_COSMOS_ENDPOINT")
        key = os.environ.get("AZURE_COSMOS_KEY")
        database_name = os.environ.get("AZURE_COSMOS_DATABASE", "identity_audit")
        container_name = os.environ.get("AZURE_COSMOS_CONTAINER", "login_audits")

        if not endpoint or not key:
            raise ValueError(
                "AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY environment variables must be set"
            )

        self.client = CosmosClient(endpoint, key)
        self.database = self.client.get_database_client(database_name)
        self.container = self.database.get_container_client(container_name)

        # Ensure database and container exist
        self._ensure_infrastructure()

    def _ensure_infrastructure(self):
        """Ensure database and container exist."""
        try:
            # Try to read database to check if it exists
            self.database.read()
        except CosmosHttpResponseError:
            # Database doesn't exist, create it
            self.client.create_database_if_not_exists(self.database.id)

        try:
            # Try to read container to check if it exists
            self.container.read()
        except CosmosHttpResponseError:
            # Container doesn't exist, create it with partition key on provider
            self.database.create_container_if_not_exists(
                id=self.container.id, partition_key=PartitionKey(path="/provider")
            )

    def store_audit_record(self, audit_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Store a single login audit record.
        """
        # Ensure record has required fields
        if "id" not in audit_record:
            import uuid

            audit_record["id"] = str(uuid.uuid4())

        if "timestamp" not in audit_record:
            audit_record["timestamp"] = datetime.utcnow().isoformat()

        if "provider" not in audit_record:
            audit_record["provider"] = "unknown"

        # Add Cosmos DB metadata
        audit_record["_partitionKey"] = audit_record["provider"]

        try:
            response = self.container.create_item(body=audit_record)
            return {
                "success": True,
                "id": response["id"],
                "provider": response["provider"],
                "timestamp": response["timestamp"],
            }
        except CosmosHttpResponseError as e:
            return {"success": False, "error": str(e), "id": audit_record.get("id")}

    def store_batch_audit_records(
        self, audit_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Store multiple login audit records in batch.
        """
        results = {"successful": 0, "failed": 0, "errors": [], "details": []}

        for record in audit_records:
            result = self.store_audit_record(record)
            results["details"].append(result)

            if result.get("success"):
                results["successful"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(result.get("error", "Unknown error"))

        return results

    def get_audit_records(
        self,
        provider: Optional[str] = None,
        user_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Query audit records with optional filters.
        """
        query_parts = ["SELECT * FROM c WHERE 1=1"]
        parameters = []

        if provider:
            query_parts.append("AND c.provider = @provider")
            parameters.append({"name": "@provider", "value": provider})

        if user_id:
            query_parts.append("AND c.user_id = @user_id")
            parameters.append({"name": "@user_id", "value": user_id})

        if status:
            query_parts.append("AND c.status = @status")
            parameters.append({"name": "@status", "value": status})

        if start_time:
            query_parts.append("AND c.timestamp >= @start_time")
            parameters.append({"name": "@start_time", "value": start_time.isoformat()})

        if end_time:
            query_parts.append("AND c.timestamp <= @end_time")
            parameters.append({"name": "@end_time", "value": end_time.isoformat()})

        query_parts.append("ORDER BY c.timestamp DESC")

        query = " ".join(query_parts)

        try:
            items = list(
                self.container.query_items(
                    query=query, parameters=parameters, max_item_count=limit
                )
            )
            return items
        except CosmosHttpResponseError as e:
            print(f"Error querying audit records: {e}")
            return []

    def get_audit_summary(
        self,
        provider: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Get summary statistics for audit records.
        """
        records = self.get_audit_records(
            provider=provider, start_time=start_time, end_time=end_time, limit=1000
        )

        total = len(records)
        success_count = sum(1 for r in records if r.get("status") == "success")
        failure_count = total - success_count

        # Count by provider
        provider_counts = {}
        for record in records:
            prov = record.get("provider", "unknown")
            provider_counts[prov] = provider_counts.get(prov, 0) + 1

        # Count by hour (for time distribution)
        hourly_counts = {}
        for record in records:
            timestamp = record.get("timestamp")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    hour = dt.strftime("%Y-%m-%d %H:00")
                    hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
                except (ValueError, TypeError):
                    pass

        return {
            "total_records": total,
            "success_count": success_count,
            "failure_count": failure_count,
            "success_rate": (success_count / total * 100) if total > 0 else 0,
            "provider_distribution": provider_counts,
            "hourly_distribution": dict(
                sorted(hourly_counts.items())[-24:]
            ),  # Last 24 hours
            "time_range": {
                "start": start_time.isoformat() if start_time else None,
                "end": end_time.isoformat() if end_time else None,
            },
        }

    def delete_old_audit_records(self, older_than_days: int = 90) -> Dict[str, Any]:
        """
        Delete audit records older than specified days.
        Returns count of deleted records.
        """
        cutoff_date = datetime.utcnow() - timedelta(days=older_than_days)

        # Get records to delete
        old_records = self.get_audit_records(end_time=cutoff_date, limit=10000)

        deleted_count = 0
        errors = []

        for record in old_records:
            try:
                self.container.delete_item(
                    item=record["id"], partition_key=record["provider"]
                )
                deleted_count += 1
            except CosmosHttpResponseError as e:
                errors.append(f"Failed to delete record {record['id']}: {e}")

        return {
            "deleted_count": deleted_count,
            "total_found": len(old_records),
            "errors": errors,
            "cutoff_date": cutoff_date.isoformat(),
        }

    def get_record_by_id(
        self, record_id: str, provider: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific audit record by ID and provider (partition key).
        """
        try:
            record = self.container.read_item(item=record_id, partition_key=provider)
            return record
        except CosmosHttpResponseError:
            return None


# Helper function for backward compatibility
def store_login_audit(audit_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to store a single login audit record.
    """
    store = LoginAuditStore()
    return store.store_audit_record(audit_record)


def query_login_audits(
    provider: Optional[str] = None,
    user_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    status: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """
    Convenience function to query login audit records.
    """
    store = LoginAuditStore()
    return store.get_audit_records(
        provider=provider,
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        status=status,
        limit=limit,
    )
