"""Persist federated-login audit records in IBM Cloudant managed document store."""

import os
import time
from typing import Optional, List, Dict, Any

from ibmcloudant import CloudantV1
from ibmcloudant.cloudant_v1 import Document, DocumentsResult

from identity_models import AuditEvent


def get_cloudant_client(
    url: Optional[str] = None,
    apikey: Optional[str] = None,
) -> CloudantV1:
    """Create an IBM Cloudant client instance."""
    cloudant_url = url or os.environ.get("IBM_CLOUDANT_URL", "https://example.cloudantnosqldb.appdomain.cloud")
    cloudant_apikey = apikey or os.environ.get("IBM_CLOUDANT_APIKEY", "")

    client = CloudantV1.new_instance(
        service_url=cloudant_url,
        authenticator={
            "type": "iam",
            "apikey": cloudant_apikey,
        } if cloudant_apikey else None,
    )
    return client


def store_audit_event(
    event: AuditEvent,
    database: str = "federated_login_audits",
    url: Optional[str] = None,
    apikey: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Persist a single federated-login audit event to IBM Cloudant.
    """
    client = get_cloudant_client(url=url, apikey=apikey)

    doc_body = event.to_document()
    doc_body["_id"] = f"audit_{event.event_type}_{int(time.time())}_{event.session_id or 'nosession'}"

    document = Document(
        **{k: v for k, v in doc_body.items() if k != "_id"},
    )
    document._id = doc_body["_id"]

    response = client.post_document(
        db=database,
        document=document,
    ).get_result()

    return {
        "doc_id": response.get("id"),
        "rev": response.get("rev"),
        "database": database,
        "provider": "IBM Cloudant",
        "success": True,
    }


def store_audit_events_bulk(
    events: List[AuditEvent],
    database: str = "federated_login_audits",
    url: Optional[str] = None,
    apikey: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Bulk persist multiple audit events to IBM Cloudant.
    """
    client = get_cloudant_client(url=url, apikey=apikey)

    documents = []
    for event in events:
        doc_body = event.to_document()
        doc_id = f"audit_{event.event_type}_{int(time.time())}_{event.session_id or 'nosession'}"
        doc = Document(**{k: v for k, v in doc_body.items() if k != "_id"})
        doc._id = doc_id
        documents.append(doc)

    response = client.post_bulk_docs(
        db=database,
        documents=documents,
    ).get_result()

    stored_count = 0
    errors = []
    for item in response.get("docs", []):
        if "ok" in item:
            stored_count += 1
        elif "error" in item:
            errors.append(item)

    return {
        "total_submitted": len(events),
        "stored_count": stored_count,
        "errors": errors,
        "database": database,
        "provider": "IBM Cloudant",
    }


def query_audit_events(
    database: str = "federated_login_audits",
    selector: Optional[Dict[str, Any]] = None,
    limit: int = 50,
    url: Optional[str] = None,
    apikey: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Query audit events from IBM Cloudant using a Mango selector.
    """
    client = get_cloudant_client(url=url, apikey=apikey)

    default_selector = {"event_type": {"$exists": True}}
    query_selector = selector or default_selector

    response = client.post_find(
        db=database,
        selector=query_selector,
        limit=limit,
    ).get_result()

    docs = []
    for doc in response.get("docs", []):
        docs.append(doc)

    return {
        "documents": docs,
        "count": len(docs),
        "database": database,
        "provider": "IBM Cloudant",
        "selector": query_selector,
    }


def query_events_by_user(
    user_sub: str,
    database: str = "federated_login_audits",
    limit: int = 50,
    url: Optional[str] = None,
    apikey: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Query audit events for a specific user from IBM Cloudant.
    """
    selector = {"user_sub": user_sub}
    return query_audit_events(
        database=database,
        selector=selector,
        limit=limit,
        url=url,
        apikey=apikey,
    )


if __name__ == "__main__":
    sample_event = AuditEvent(
        event_type="login_attempt",
        timestamp=time.time(),
        user_sub="user_test_001",
        client_id="test_client",
        provider="Google Identity Platform",
        ip_address="192.168.1.100",
        success=True,
        session_id="sess_test_001",
    )
    print("Sample audit event document:", sample_event.to_document())
