def summarize_rotation_status(rotation_logs):
    return {'status': 'success' if rotation_logs else 'failed'}