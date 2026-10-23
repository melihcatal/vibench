import json

def store_audit_record(record):
    with open('audit_records.json', 'a') as f:
        json.dump(record, f)
        f.write('\n')