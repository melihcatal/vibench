import json

def login_audit_store(audit_record):
    with open('audit_records.json', 'a') as f:
        json.dump(audit_record, f)
        f.write('\n')