import json
from security_client import SecurityClient
from security_models import SecretResponse


def fetch_db_secret(secret_name: str = "prod/db-secret") -> str:
    client = SecurityClient()
    response: SecretResponse = client.get_secret(secret_name)
    db_config = json.loads(response.value)
    connection_string = (
        f"{db_config['engine']}://"
        f"{db_config['username']}:{db_config['password']}@"
        f"{db_config['host']}:{db_config.get('port', 5432)}/"
        f"{db_config['dbname']}"
    )
    return connection_string
