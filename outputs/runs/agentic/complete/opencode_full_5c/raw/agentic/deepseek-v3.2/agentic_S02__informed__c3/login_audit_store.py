import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class LoginAuditStore:
    def __init__(self):
        service_url = os.environ.get("IBM_CLOUDANT_URL")
        api_key = os.environ.get("IBM_CLOUDANT_APIKEY")

        if not service_url or not api_key:
            raise ValueError(
                "IBM_CLOUDANT_URL and IBM_CLOUDANT_APIKEY environment variables are required"
            )

        authenticator = IAMAuthenticator(api_key)
        self.client = CloudantV1(authenticator=authenticator)
        self.client.set_service_url(service_url)

        self.database_name = "login_audit_logs"
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        try:
            self.client.get_database_information(db=self.database_name)
        except Exception:
            self.client.put_database(db=self.database_name)

    def store_login_event(self, event_data: Dict[str, Any]) -> str:
        document = Document(**event_data)

        response = self.client.post_document(
            db=self.database_name, document=document
        ).get_result()

        return response["id"]

    def store_batch_events(self, events: List[Dict[str, Any]]) -> List[str]:
        docs = []
        for event in events:
            doc = Document(**event)
            docs.append(doc)

        response = self.client.post_bulk_docs(
            db=self.database_name, bulk_docs={"docs": docs}
        ).get_result()

        doc_ids = [item["id"] for item in response]
        return doc_ids

    def get_event(self, doc_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.client.get_document(
                db=self.database_name, doc_id=doc_id
            ).get_result()

            return dict(response)
        except Exception:
            return None

    def query_events(
        self, selector: Dict[str, Any], limit: int = 100
    ) -> List[Dict[str, Any]]:
        response = self.client.post_find(
            db=self.database_name, selector=selector, limit=limit
        ).get_result()

        return response["docs"]

    def get_events_by_user(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        selector = {"user_id": user_id}

        return self.query_events(selector, limit)

    def get_events_by_provider(
        self, provider: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        selector = {"provider": provider}

        return self.query_events(selector, limit)

    def get_failed_logins(self, hours: int = 24) -> List[Dict[str, Any]]:
        from datetime import datetime, timedelta

        time_threshold = (datetime.utcnow() - timedelta(hours=hours)).isoformat()

        selector = {"success": False, "timestamp": {"$gt": time_threshold}}

        return self.query_events(selector, limit=200)

    def create_login_event(
        self,
        user_id: str,
        provider: str,
        success: bool,
        ip_address: str,
        user_agent: str,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        event = {
            "type": "login_attempt",
            "user_id": user_id,
            "provider": provider,
            "success": success,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "timestamp": datetime.utcnow().isoformat(),
            "stored_at": datetime.utcnow().isoformat(),
            "storage_provider": "ibm_cloudant",
        }

        if additional_data:
            event.update(additional_data)

        return event

    def store_login_attempt(
        self,
        user_id: str,
        provider: str,
        success: bool,
        ip_address: str,
        user_agent: str,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        event = self.create_login_event(
            user_id=user_id,
            provider=provider,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
            additional_data=additional_data,
        )

        doc_id = self.store_login_event(event)
        return doc_id

    def get_statistics(self, days: int = 7) -> Dict[str, Any]:
        from datetime import datetime, timedelta

        time_threshold = (datetime.utcnow() - timedelta(days=days)).isoformat()

        selector = {"timestamp": {"$gt": time_threshold}}

        events = self.query_events(selector, limit=1000)

        stats = {
            "total_attempts": len(events),
            "successful_logins": sum(1 for e in events if e.get("success")),
            "failed_logins": sum(1 for e in events if not e.get("success")),
            "unique_users": len(
                set(e.get("user_id") for e in events if e.get("user_id"))
            ),
            "providers": {},
            "time_period_days": days,
        }

        for event in events:
            provider = event.get("provider", "unknown")
            stats["providers"][provider] = stats["providers"].get(provider, 0) + 1

        if stats["total_attempts"] > 0:
            stats["success_rate"] = (
                stats["successful_logins"] / stats["total_attempts"]
            ) * 100
        else:
            stats["success_rate"] = 0

        return stats

    def cleanup_old_events(self, days_to_keep: int = 90):
        from datetime import datetime, timedelta

        cutoff_date = (datetime.utcnow() - timedelta(days=days_to_keep)).isoformat()

        selector = {"timestamp": {"$lt": cutoff_date}}

        old_events = self.query_events(selector, limit=1000)

        for event in old_events:
            try:
                self.client.delete_document(
                    db=self.database_name, doc_id=event["_id"], rev=event["_rev"]
                )
            except Exception:
                pass

        return len(old_events)
