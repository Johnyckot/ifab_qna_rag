from typing import Dict, List, Tuple, Union

import numpy as np
from elasticsearch import Elasticsearch

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter



@data_exporter
def elasticsearch(
    documents: List[Dict[str, Union[Dict, List[int], np.ndarray, str]]], *args, **kwargs,
):
    """
    Exports document data to an Elasticsearch database.
    """

    print(len(documents))

    es_client = Elasticsearch('http://elasticsearch:9200')
    index_name = 'idx_ifab_docs'


    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "id": {"type": "text"},
                "url": {"type": "text"},
                "h1": {"type": "text"},
                "h2": {"type": "text"},
                "h3": {"type": "text"},
                "text": {"type": "text"},
                "full_text": {"type": "text"},
                "embedding": {"type": "dense_vector", "dims": 768, "index": True, "similarity": "cosine"},
            }
        }
    }

    es_client.indices.delete(index=index_name, ignore_unavailable=True)
    es_client.indices.create(index=index_name, body=index_settings)


    for doc in documents:
        try:
            es_client.index(index=index_name, document=doc)
        except Exception as e:
            print(e)
   
