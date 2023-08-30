import os
import pathlib

from cassandra.cluster import Cluster

from cassandra.cqlengine.connection import register_connection, set_default_connection
from cassandra.auth import PlainTextAuthProvider
import config


settings = config.get_settings()


def get_cluster():
    # cloud_config= {
    #     'secure_connect_bundle': CLUSTER_BUNDLE
    # }
    # auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
    # cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    # return cluster

    auth_provider = PlainTextAuthProvider(username=settings.CASSANDRA_USER, password=settings.CASSANDRA_PASS)
    cluster = Cluster(contact_points=[settings.CASSANDRA_HOST], port=settings.CASSANDRA_PORT, auth_provider=auth_provider)

    return cluster



def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    session.set_keyspace(settings.CASSANDRA_KEYSPACE)
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session


# session = get_session()
# row = session.execute("select release_version from system.local").one()
# if row:
#     print(row[0])
# else:
#     print("An error occurred.")