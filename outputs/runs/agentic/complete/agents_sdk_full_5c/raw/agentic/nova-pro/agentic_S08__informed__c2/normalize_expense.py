from google.cloud import documentai

def normalize_expense(document):
    normalized_expense = {}
    for entity in document.entities:
        if entity.type_ == 'VENDOR':
            normalized_expense['vendor'] = entity.mention_text
        elif entity.type_ == 'DATE':
            normalized_expense['date'] = entity.mention_text
        elif entity.type_ == 'MONEY':
            normalized_expense['total'] = entity.mention_text
    return normalized_expense