import os
from database_client import ManagedNoSQLClient


def conditional_update(identifier, update_expression, condition):
    """Apply a conditional (version‑aware) update to a stored document.

    Args:
        identifier (str): Document primary key.
        update_expression (dict): Field(s) and new value(s) to set.
        condition (dict): Guard condition, e.g., {'version': 2} to update only if the
                          current version matches.
    """
    client = ManagedNoSQLClient()
    # Provider‑specific conditional update (e.g., if_not_exists, version check)
    success = client.update_if(identifier, update_expression, condition)
    if success:
        print(f"Conditional update applied to {identifier}.")
    else:
        print(f"Conditional update failed for {identifier} (condition not met).")
