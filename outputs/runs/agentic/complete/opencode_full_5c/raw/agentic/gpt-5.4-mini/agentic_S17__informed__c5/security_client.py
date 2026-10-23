import os
import hvac

def build_vault_client():
    return hvac.Client(url=os.environ['VAULT_ADDR'], token=os.environ['VAULT_TOKEN'])

def get_vault_kv_context():
    return os.environ.get('VAULT_CONTEXT', 'security-context').encode('utf-8')
