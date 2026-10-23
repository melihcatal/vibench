# helper file: security_models.py
from dataclasses import dataclass

@dataclass
class DatabaseCredentials:
    """
    A structured representation of database connection details
    retrieved from a secret store.
    """
    username: str
    password: str
    host: str
    port: int
    dbname: str

@dataclass
class SafetyClassification:
    """
    Represents the result of a safety check on secret metadata.
    """
    input_text: str
    classification: str
    confidence: float
