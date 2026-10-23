&quot;&quot;&quot;
Persists federated-login audit records in MongoDB Atlas.
&quot;&quot;&quot;
import os
import pymongo
from typing import Dict, Any
from datetime import datetime

MONGODB_ATLAS_URI = os.getenv(&#x27;MONGODB_ATLAS_URI&#x27;)

client = pymongo.MongoClient(MONGODB_ATLAS_URI)
db = client[&#x27;federated_login_audit&#x27;]
collection = db[&#x27;audit_events&#x27;]

# Ensure index
collection.create_index([(&quot;timestamp&quot;, pymongo.DESCENDING), (&quot;user_id&quot;, 1)])

def store_login_audit(event: Dict[str, Any]) -&gt; None:
    &quot;&quot;&quot;
    Stores an audit record.
    &quot;&quot;&quot;
    event.setdefault(&#x27;timestamp&#x27;, datetime.utcnow().isoformat())
    collection.insert_one(event)