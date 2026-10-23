# [LATER-STEP] rotation_summary.py
from security_models import RotationStatus, SecretReference

def summarize_rotation(secret: SecretReference) -> RotationStatus:
    """Produce a concise summary of rotation status for a given secret.

    Args:
        secret (SecretReference): Reference to the secret.

    Returns:
        RotationStatus: Populated summary object.
    """
    # Placeholder: in a real implementation this would query rotation metadata
    return RotationStatus(
        secret_name=secret.name,
        current_version="latest",
        next_rotation_due="2025-12-31T00:00:00Z",
        is_stage_complete=True,
    )
