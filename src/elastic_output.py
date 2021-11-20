import os
import uuid
from datetime import datetime
from elasticsearch import Elasticsearch

es_endpoint_scheme = os.getenv("ES_ENDPOINT_SCHEME", "https")
es_endpoint_port = os.getenv("ES_ENDPOINT_PORT", "443")
es_endpoint = os.getenv("ES_ENDPOINT")
es_username = os.getenv("ES_USERNAME")
es_password = os.getenv("ES_PASSWORD")
es_root_index = os.getenv("ES_INDEX")

es = Elasticsearch(
    [es_endpoint],
    http_auth=(es_username, es_password),
    scheme=es_endpoint_scheme,
    port=int(es_endpoint_port),
)

def index_repo_stat(document_type: str, document_body: dict, es_repo_index: str):
	document_body["@timestamp"] = datetime.now().utcnow()
	return es.index(
			index = f"{es_root_index}_{es_repo_index}",
			doc_type = document_type,
			id = uuid.uuid4(),
			body = document_body
	)