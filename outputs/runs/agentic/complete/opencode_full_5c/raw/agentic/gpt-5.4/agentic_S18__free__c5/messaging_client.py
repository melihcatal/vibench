from __future__ import annotations

import os
from functools import lru_cache

from google.cloud import pubsub_v1
from google.cloud import translate_v2 as translate
from google.cloud import language_v2
from openai import OpenAI
from supabase import Client, create_client


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def gcp_project_id() -> str:
    return require_env("GOOGLE_CLOUD_PROJECT")


def pubsub_topic_path(topic_id: str | None = None) -> str:
    publisher = get_pubsub_publisher()
    return publisher.topic_path(
        gcp_project_id(), topic_id or require_env("PUBSUB_TOPIC_ID")
    )


def pubsub_subscription_path(subscription_id: str | None = None) -> str:
    subscriber = get_pubsub_subscriber()
    return subscriber.subscription_path(
        gcp_project_id(), subscription_id or require_env("PUBSUB_SUBSCRIPTION_ID")
    )


def dead_letter_topic_path() -> str:
    publisher = get_pubsub_publisher()
    return publisher.topic_path(
        gcp_project_id(), require_env("PUBSUB_DEAD_LETTER_TOPIC_ID")
    )


@lru_cache(maxsize=1)
def get_pubsub_publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def get_pubsub_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=require_env("OPENAI_API_KEY"))


@lru_cache(maxsize=1)
def get_translate_client() -> translate.Client:
    return translate.Client()


@lru_cache(maxsize=1)
def get_language_client() -> language_v2.LanguageServiceClient:
    return language_v2.LanguageServiceClient()


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    return create_client(
        require_env("SUPABASE_URL"), require_env("SUPABASE_SERVICE_ROLE_KEY")
    )


def audit_table_name() -> str:
    return os.getenv("SUPABASE_AUDIT_TABLE", "message_audit")
