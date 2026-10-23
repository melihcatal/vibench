import datetime
import json
import os
from typing import List, Dict
from google.cloud import datastore

datastore_client = datastore.Client(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
KIND = 'OnboardingEvent'

def summarize_onboarding(user_id: str) -> Dict[str, any]:
    """Retrieve onboarding state for a user and compile a concise support summary.
    Returns a dict containing timestamps, completed steps, moderation status, and notes.
    """
    # 1. Collect profile moderation status
    profile_key = datastore_client.key('ProfileText', user_id)
    profile = datastore_client.get(profile_key)
    moderation_status = 'pending' if not profile else ('approved' if profile.get('moderation_status') == 'approved' else 'rejected')
    
    # 2. Gather onboarding events
    query = datastore_client.query(kind=KIND)
    query.add_filter('user_id', '=', user_id)
    events = list(query.fetch())
    completed_steps = [e['step'] for e in events if e['completed']]
    
    # 3. Compile summary
    summary = {
        'user_id': user_id,
        'profile_moderation': moderation_status,
        'completed_steps': completed_steps,
        'last_login': get_last_login(user_id),
        'notes': get_notes(user_id)
    }
    return summary

def get_last_login(user_id: str) -> str:
    """Helper: fetch most recent login timestamp from Activity events."""
    query = datastore_client.query(kind='Activity')
    query.add_filter('user_id', '=', user_id)
    query.order = ['-timestamp']
    result = list(query.fetch(limit=1))
    if result:
        return result[0]['timestamp'].isoformat()
    return 'never'

def get_notes(user_id: str) -> List[Dict]:
    """Helper: retrieve stored notes from the document store."""
    notes = []
    query = datastore_client.query(kind='ProfileNote')
    query.add_filter('user_id', '=', user_id)
    for note in query.fetch():
        notes.append(json.loads(note['payload']))
    return notes
