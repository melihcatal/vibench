import os
import time
from pymongo import MongoClient
from identity_client import (
    MONGODB_ATLAS_URI,
    MONGODB_ATLAS_DB,
    MONGODB_ATLAS_AUDIT_COLLECTION,
)
from identity_models import AuditEvent


def _get_mongo_client(uri=None):
    if not uri:
        uri = MONGODB_ATLAS_URI
    return MongoClient(uri)


def persist_audit_event(event, db_name=None, collection_name=None, uri=None):
    if not db_name:
        db_name = MONGODB_ATLAS_DB
    if not collection_name:
        collection_name = MONGODB_ATLAS_AUDIT_COLLECTION
    client = _get_mongo_client(uri)
    db = client[db_name]
    collection = db[collection_name]
    document = {
        "event_type": event.event_type,
        "subject": event.subject,
        "provider": event.provider,
        "timestamp": event.timestamp,
        "details": event.details,
        "ip_address": event.ip_address,
        "user_agent": event.user_agent,
        "created_at": time.time(),
        "created_at_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    result = collection.insert_one(document)
    client.close()
    return str(result.inserted_id)


def persist_audit_events(events, db_name=None, collection_name=None, uri=None):
    if not db_name:
        db_name = MONGODB_ATLAS_DB
    if not collection_name:
        collection_name = MONGODB_ATLAS_AUDIT_COLLECTION
    client = _get_mongo_client(uri)
    db = client[db_name]
    collection = db[collection_name]
    documents = []
    for event in events:
        documents.append(
            {
                "event_type": event.event_type,
                "subject": event.subject,
                "provider": event.provider,
                "timestamp": event.timestamp,
                "details": event.details,
                "ip_address": event.ip_address,
                "user_agent": event.user_agent,
                "created_at": time.time(),
                "created_at_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
        )
    result = collection.insert_many(documents)
    client.close()
    return [str(i) for i in result.inserted_ids]


def query_audit_events(
    subject=None,
    provider=None,
    event_type=None,
    start_time=None,
    end_time=None,
    limit=100,
    db_name=None,
    collection_name=None,
    uri=None,
):
    if not db_name:
        db_name = MONGODB_ATLAS_DB
    if not collection_name:
        collection_name = MONGODB_ATLAS_AUDIT_COLLECTION
    client = _get_mongo_client(uri)
    db = client[db_name]
    collection = db[collection_name]
    query = {}
    if subject:
        query["subject"] = subject
    if provider:
        query["provider"] = provider
    if event_type:
        query["event_type"] = event_type
    if start_time is not None or end_time is not None:
        time_filter = {}
        if start_time is not None:
            time_filter["$gte"] = start_time
        if end_time is not None:
            time_filter["$lte"] = end_time
        query["timestamp"] = time_filter
    cursor = collection.find(query).sort("timestamp", -1).limit(limit)
    events = []
    for doc in cursor:
        events.append(
            AuditEvent(
                event_type=doc.get("event_type", ""),
                subject=doc.get("subject", ""),
                provider=doc.get("provider", ""),
                timestamp=doc.get("timestamp", 0),
                details=doc.get("details", {}),
                ip_address=doc.get("ip_address"),
                user_agent=doc.get("user_agent"),
            )
        )
    client.close()
    return events
