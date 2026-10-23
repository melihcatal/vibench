from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from pymongo import MongoClient
from pymongo.collection import Collection


@dataclass(slots=True)
class Auth0Config:
    domain: str
    client_id: str
    client_secret: str
    audience: Optional[str] = None
    database_connection: str = "Username-Password-Authentication"
    timeout_seconds: int = 30

    @property
    def base_url(self) -> str:
        return f"https://{self.domain}"


@dataclass(slots=True)
class MongoAtlasConfig:
    uri: str
    database: str
    collection: str


class Auth0Client:
    def __init__(self, config: Auth0Config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.config.base_url}{path}",
            json=payload,
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {}


class MongoAtlasNoteStore:
    def __init__(self, config: MongoAtlasConfig):
        self.client = MongoClient(config.uri)
        self.collection: Collection = self.client[config.database][config.collection]

    def upsert_profile_note(self, document: Dict[str, Any]) -> Dict[str, Any]:
        result = self.collection.update_one(
            {"user_id": document["user_id"]},
            {"$set": document},
            upsert=True,
        )
        return {
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "upserted_id": str(result.upserted_id) if result.upserted_id is not None else None,
        }


def load_auth0_config() -> Auth0Config:
    return Auth0Config(
        domain=os.environ["AUTH0_DOMAIN"],
        client_id=os.environ["AUTH0_CLIENT_ID"],
        client_secret=os.environ["AUTH0_CLIENT_SECRET"],
        audience=os.getenv("AUTH0_AUDIENCE"),
        database_connection=os.getenv("AUTH0_DB_CONNECTION", "Username-Password-Authentication"),
        timeout_seconds=int(os.getenv("AUTH0_TIMEOUT_SECONDS", "30")),
    )



def load_mongodb_atlas_config() -> MongoAtlasConfig:
    return MongoAtlasConfig(
        uri=os.environ["MONGODB_ATLAS_URI"],
        database=os.getenv("MONGODB_ATLAS_DATABASE", "identity_app"),
        collection=os.getenv("MONGODB_ATLAS_COLLECTION", "profile_notes"),
    )
