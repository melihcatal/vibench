import os
from typing import Optional
from datetime import datetime, timezone, timedelta

import requests
from elasticsearch import Elasticsearch

from identity_models import AuditRecord, AuditEventType


PROVIDER = "elasticsearch"
ELASTICSEARCH_HOSTS = os.environ.get("ELASTICSEARCH_HOSTS", "https://localhost:9200")
ELASTICSEARCH_API_KEY = os.environ.get("ELASTICSEARCH_API_KEY", "")
ELASTICSEARCH_CLOUD_ID = os.environ.get("ELASTICSEARCH_CLOUD_ID", "")
AUDIT_INDEX = os.environ.get("ELASTIC_AUDIT_INDEX", "federated-login-audit")


def get_es_client() -> Elasticsearch:
    if ELASTICSEARCH_CLOUD_ID:
        return Elasticsearch(
            cloud_id=ELASTICSEARCH_CLOUD_ID,
            api_key=ELASTICSEARCH_API_KEY,
        )
    return Elasticsearch(
        hosts=[ELASTICSEARCH_HOSTS],
        api_key=ELASTICSEARCH_API_KEY,
        verify_certs=True,
    )


def store_audit_event(
    audit_record: AuditRecord,
    es_client: Optional[Elasticsearch] = None,
    index: Optional[str] = None,
) -> dict:
    client = es_client or get_es_client()
    idx = index or AUDIT_INDEX
    doc = audit_record.to_dict()
    doc["@timestamp"] = audit_record.timestamp.isoformat()
    response = client.index(index=idx, document=doc)
    return {
        "document_id": response["id"],
        "index": idx,
        "result": response["result"],
    }


def summarize_login_events(
    days: int = 30,
    es_client: Optional[Elasticsearch] = None,
    index: Optional[str] = None,
) -> dict:
    client = es_client or get_es_client()
    idx = index or AUDIT_INDEX
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    query = {
        "size": 0,
        "query": {
            "range": {
                "@timestamp": {
                    "gte": start_date.isoformat(),
                    "lte": datetime.now(timezone.utc).isoformat(),
                }
            }
        },
        "aggs": {
            "event_types": {"terms": {"field": "event_type.keyword", "size": 50}},
            "success_vs_failure": {"terms": {"field": "success", "size": 2}},
            "providers": {"terms": {"field": "provider.keyword", "size": 20}},
            "daily_logins": {
                "date_histogram": {
                    "field": "@timestamp",
                    "calendar_interval": "day",
                },
                "aggs": {
                    "successful": {"filter": {"term": {"success": True}}},
                    "failed": {"filter": {"term": {"success": False}}},
                },
            },
            "unique_users": {"cardinality": {"field": "user_id.keyword"}},
            "unique_sessions": {"cardinality": {"field": "session_id.keyword"}},
        },
    }
    response = client.search(index=idx, body=query)
    aggregations = response["aggregations"]
    event_type_counts = {
        bucket["key"]: bucket["doc_count"]
        for bucket in aggregations["event_types"]["buckets"]
    }
    success_counts = {
        str(bucket["key"]): bucket["doc_count"]
        for bucket in aggregations["success_vs_failure"]["buckets"]
    }
    provider_counts = {
        bucket["key"]: bucket["doc_count"]
        for bucket in aggregations["providers"]["buckets"]
    }
    daily_data = []
    for bucket in aggregations["daily_logins"]["buckets"]:
        daily_data.append(
            {
                "date": bucket["key_as_string"],
                "total": bucket["doc_count"],
                "successful": bucket["successful"]["doc_count"],
                "failed": bucket["failed"]["doc_count"],
            }
        )
    total_events = sum(event_type_counts.values())
    total_successful = int(success_counts.get("True", 0))
    total_failed = int(success_counts.get("False", 0))
    success_rate = (total_successful / total_events * 100) if total_events > 0 else 0
    return {
        "provider": PROVIDER,
        "elasticsearch_index": idx,
        "period_days": days,
        "summary": {
            "total_events": total_events,
            "total_successful": total_successful,
            "total_failed": total_failed,
            "success_rate_pct": round(success_rate, 2),
            "unique_users": aggregations["unique_users"]["value"],
            "unique_sessions": aggregations["unique_sessions"]["value"],
        },
        "event_type_breakdown": event_type_counts,
        "provider_breakdown": provider_counts,
        "daily_trend": daily_data,
    }


def get_recent_failures(
    limit: int = 50,
    hours: int = 24,
    es_client: Optional[Elasticsearch] = None,
    index: Optional[str] = None,
) -> list[dict]:
    client = es_client or get_es_client()
    idx = index or AUDIT_INDEX
    start_date = datetime.now(timezone.utc) - timedelta(hours=hours)
    query = {
        "size": limit,
        "query": {
            "bool": {
                "must": [
                    {"term": {"success": False}},
                    {
                        "range": {
                            "@timestamp": {
                                "gte": start_date.isoformat(),
                            }
                        }
                    },
                ]
            }
        },
        "sort": [{"@timestamp": {"order": "desc"}}],
    }
    response = client.search(index=idx, body=query)
    return [
        {
            "event_id": hit["_source"].get("event_id"),
            "event_type": hit["_source"].get("event_type"),
            "user_id": hit["_source"].get("user_id"),
            "error_message": hit["_source"].get("error_message"),
            "timestamp": hit["_source"].get("@timestamp"),
            "provider": hit["_source"].get("provider"),
        }
        for hit in response["hits"]["hits"]
    ]


def get_user_login_history(
    user_id: str,
    limit: int = 100,
    es_client: Optional[Elasticsearch] = None,
    index: Optional[str] = None,
) -> list[dict]:
    client = es_client or get_es_client()
    idx = index or AUDIT_INDEX
    query = {
        "size": limit,
        "query": {"term": {"user_id.keyword": user_id}},
        "sort": [{"@timestamp": {"order": "desc"}}],
    }
    response = client.search(index=idx, body=query)
    return [hit["_source"] for hit in response["hits"]["hits"]]
