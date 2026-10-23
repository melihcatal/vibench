def rotation_summary(rotations):
    """Produce a concise summary of secret rotation status.
    rotations: list of dicts with keys: name, rotated (bool), last_rotated (ISO8601 or None)
    Returns a string summary.
    """
    total = len(rotations)
    rotated = sum(1 for r in rotations if r.get('rotated'))
    summary = f"Secret rotation check:\n  Total secrets: {total}\n  Successfully rotated: {rotated}\n  Pending rotation: {total - rotated}"
    return summary
