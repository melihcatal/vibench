"""
Persist onboarding notes and support metadata in a managed document store
using Firebase Firestore.

Provider: Firebase Firestore (google-cloud-firestore SDK)
Concrete provider signals: google.cloud.firestore, firestore.googleapis.com,
                           FIRESTORE_DATABASE_ID, GOOGLE_APPLICATION_CREDENTIALS.
"""

import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

from google.cloud import firestore


logger = logging.getLogger(__name__)

# Firebase Firestore provider configuration
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-firestore-project")
FIRESTORE_DATABASE_ID = os.environ.get("FIRESTORE_DATABASE_ID", "(default)")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")

# Firestore collection names
ONBOARDING_NOTES_COLLECTION = "onboarding_notes"
SUPPORT_METADATA_COLLECTION = "support_metadata"
USER_PROFILES_COLLECTION = "user_profiles"


def get_firestore_client(project_id: Optional[str] = None) -> firestore.Client:
    """
    Create a Firestore client connected to the Firebase Firestore backend.
    
    Uses the google-cloud-firestore SDK which communicates with:
    https://firestore.googleapis.com
    
    Args:
        project_id: Optional Google Cloud project ID.
        
    Returns:
        Configured Firestore client instance.
    """
    target_project = project_id or GOOGLE_CLOUD_PROJECT
    return firestore.Client(project=target_project, database=FIRESTORE_DATABASE_ID)


def persist_onboarding_note(
    user_id: str,
    note: str,
    note_type: str = "general",
    metadata: Optional[Dict[str, Any]] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Persist an onboarding note for a user in Firebase Firestore.
    
    Stores the note in the 'onboarding_notes' collection under the user's
    document in Firebase Firestore (firestore.googleapis.com).
    
    Args:
        user_id: The user's unique identifier.
        note: The note content.
        note_type: Type of note (e.g., "general", "support", "moderation", "translation").
        metadata: Optional additional metadata.
        project_id: Optional Google Cloud project ID.
        
    Returns:
        Dict with success status and document reference.
    """
    try:
        db = get_firestore_client(project_id)
        
        doc_data = {
            "user_id": user_id,
            "note": note,
            "note_type": note_type,
            "metadata": metadata or {},
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP,
            "provider": "firebase_firestore",
        }
        
        doc_ref = db.collection(ONBOARDING_NOTES_COLLECTION).document()
        doc_ref.set(doc_data)
        
        logger.info(
            "Firebase Firestore note persisted: user_id=%s, doc_id=%s (database: %s)",
            user_id,
            doc_ref.id,
            FIRESTORE_DATABASE_ID,
        )
        
        return {
            "success": True,
            "document_id": doc_ref.id,
            "collection": ONBOARDING_NOTES_COLLECTION,
            "user_id": user_id,
            "provider": "firebase_firestore",
        }
        
    except Exception as e:
        logger.error("Firebase Firestore persist error: %s", str(e))
        return {
            "success": False,
            "error": "FIRESTORE_ERROR",
            "message": str(e),
            "provider": "firebase_firestore",
        }


def persist_support_metadata(
    user_id: str,
    metadata: Dict[str, Any],
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Persist support metadata for a user in Firebase Firestore.
    
    Stores metadata in the 'support_metadata' collection in Firestore
    (firestore.googleapis.com).
    
    Args:
        user_id: The user's unique identifier.
        metadata: Dict of support metadata fields.
        project_id: Optional Google Cloud project ID.
        
    Returns:
        Dict with success status and document reference.
    """
    try:
        db = get_firestore_client(project_id)
        
        doc_data = {
            "user_id": user_id,
            "metadata": metadata,
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP,
            "provider": "firebase_firestore",
        }
        
        doc_ref = db.collection(SUPPORT_METADATA_COLLECTION).document(user_id)
        doc_ref.set(doc_data, merge=True)
        
        logger.info(
            "Firebase Firestore support metadata persisted: user_id=%s (database: %s)",
            user_id,
            FIRESTORE_DATABASE_ID,
        )
        
        return {
            "success": True,
            "document_id": doc_ref.id,
            "collection": SUPPORT_METADATA_COLLECTION,
            "user_id": user_id,
            "provider": "firebase_firestore",
        }
        
    except Exception as e:
        logger.error("Firebase Firestore metadata persist error: %s", str(e))
        return {
            "success": False,
            "error": "FIRESTORE_ERROR",
            "message": str(e),
            "provider": "firebase_firestore",
        }


def get_user_onboarding_notes(
    user_id: str,
    limit: int = 50,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve onboarding notes for a user from Firebase Firestore.
    
    Queries the 'onboarding_notes' collection in Firestore.
    
    Args:
        user_id: The user's unique identifier.
        limit: Maximum number of notes to return.
        project_id: Optional Google Cloud project ID.
        
    Returns:
        Dict with notes list and metadata.
    """
    try:
        db = get_firestore_client(project_id)
        
        query = (
            db.collection(ONBOARDING_NOTES_COLLECTION)
            .where("user_id", "==", user_id)
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .limit(limit)
        )
        
        docs = query.stream()
        notes = []
        
        for doc in docs:
            note_data = doc.to_dict()
            note_data["document_id"] = doc.id
            notes.append(note_data)
        
        logger.info(
            "Firebase Firestore notes retrieved: user_id=%s, count=%d (database: %s)",
            user_id,
            len(notes),
            FIRESTORE_DATABASE_ID,
        )
        
        return {
            "success": True,
            "notes": notes,
            "count": len(notes),
            "user_id": user_id,
            "provider": "firebase_firestore",
        }
        
    except Exception as e:
        logger.error("Firebase Firestore query error: %s", str(e))
        return {
            "success": False,
            "error": "FIRESTORE_ERROR",
            "message": str(e),
            "provider": "firebase_firestore",
        }


def persist_full_onboarding_record(
    user_id: str,
    onboarding_data: Dict[str, Any],
    moderation_results: Optional[Dict[str, Any]] = None,
    translation_locale: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Persist a complete onboarding record including notes, moderation, and
    translation data in Firebase Firestore.
    
    Creates documents in multiple collections in a single Firestore database
    (firestore.googleapis.com).
    
    Args:
        user_id: The user's unique identifier.
        onboarding_data: Full onboarding state data.
        moderation_results: Optional moderation API results.
        translation_locale: User's selected locale for translations.
        project_id: Optional Google Cloud project ID.
        
    Returns:
        Dict with success status and document references.
    """
    results = {
        "success": True,
        "user_id": user_id,
        "documents": {},
        "provider": "firebase_firestore",
    }
    
    try:
        db = get_firestore_client(project_id)
        
        profile_doc = {
            "user_id": user_id,
            "onboarding_completed": onboarding_data.get("onboarding_completed", False),
            "locale": translation_locale or "en",
            "onboarding_data": onboarding_data,
            "moderation_results": moderation_results,
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP,
            "provider": "firebase_firestore",
        }
        
        profile_ref = db.collection(USER_PROFILES_COLLECTION).document(user_id)
        profile_ref.set(profile_doc, merge=True)
        results["documents"]["profile"] = profile_ref.id
        
        if moderation_results and not moderation_results.get("approved", True):
            note_text = f"Profile moderation flagged: {moderation_results.get('flagged_fields', [])}"
            note_result = persist_onboarding_note(
                user_id=user_id,
                note=note_text,
                note_type="moderation",
                metadata={"moderation_results": moderation_results},
                project_id=project_id,
            )
            results["documents"]["moderation_note"] = note_result.get("document_id")
        
        logger.info(
            "Firebase Firestore full onboarding record persisted: user_id=%s (database: %s)",
            user_id,
            FIRESTORE_DATABASE_ID,
        )
        
        return results
        
    except Exception as e:
        logger.error("Firebase Firestore full record persist error: %s", str(e))
        results["success"] = False
        results["error"] = "FIRESTORE_ERROR"
        results["message"] = str(e)
        return results
