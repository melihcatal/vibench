import os
import json
from database_client import get_client


def conditional_update(identifier, update_ops, expected_version=None):
    """Apply a conditional/version-aware update to a stored document.

    Uses the provider's CAS/match operator to ensure the update occurs only if the document hasn't changed since the given version.
    Returns the updated document or raises an exception if the condition fails.
    """
    client = get_client()
    response = client.update_document(
        identifier=identifier, update_ops=update_ops, version=expected_version
    )
    return response
