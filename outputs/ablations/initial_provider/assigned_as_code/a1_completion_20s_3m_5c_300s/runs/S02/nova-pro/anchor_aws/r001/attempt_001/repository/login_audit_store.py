import json


def persist_audit_record(record, store):
    store.append(record)


def get_audit_store():
    return []