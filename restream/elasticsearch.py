"""
Elasticsearch batch re-streamer
"""
import time
import datetime
import sys

import numpy as np

import elasticsearch

from elasticsearch.helpers import bulk

from ..exceptions import ElasticsearchConnectionError


def init_elasticsearch(uri):
    # init ElasticSearch
    es_conn = elasticsearch.Elasticsearch(uri)
    try:
        es_conn.info()
    except elasticsearch.ConnectionError:
        raise ElasticsearchConnectionError(uri)

    return es_conn
