import google.cloud.documentai as documentai

def normalize_expense(expense):
    # Normalize expense fields into a standard JSON schema
    return {'vendor': expense['vendor'], 'date': expense['date'], 'total': expense['total'], 'items': expense['line_items']}