def summarize_embedding_job(results: dict) -> str:
    """Create a concise summary of an embedding job run.
    Expected `results` dict contains keys:
        - 'status': 'success' or 'error'
        - 'count': number of texts processed
        - 'duration_seconds': runtime
        - 'errors': list of error messages (if any)
    Returns a plain‑text summary string.
    """
    status = results.get('status', 'unknown')
    count = results.get('count', 0)
    duration = results.get('duration_seconds', 0)
    errors = results.get('errors', [])
    lines = [f'Embedding job completed: {status}']
    lines.append(f'Processed {count} text{s:plural(count)}')
    lines.append(f'Runtime: {duration:.2f} seconds')
    if errors:
        lines.append('Errors encountered:')
        for err in errors:
            lines.append(f'  - {err}')
    return '\n'.join(lines)

from inflection import pluralize as plural
# Note: using the `inflection` library to generate singular/plural forms automatically.
