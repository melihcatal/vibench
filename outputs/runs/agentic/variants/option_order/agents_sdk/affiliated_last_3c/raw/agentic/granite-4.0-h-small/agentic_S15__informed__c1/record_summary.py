from database_models import DocumentModel


def summarize(doc):
    '''Return a concise human‑readable summary of a document dictionary.'''
    if isinstance(doc, dict):
        title = doc.get('title', 'Untitled')
        excerpt = doc.get('content', '')[:100]
        summary = f"Title: {title}\nExcerpt: {excerpt}"
        return summary
    return 'No document provided'

# Example usage (local):
# print(summarize(fetch_document('my-doc-id')))  # when fetch_document returns a dict
# or wrap fetch_document to convert boto3 Item to dict:
# summary = summarize({k: v['S'] for k, v in fetch_document('my-doc-id').items()})
