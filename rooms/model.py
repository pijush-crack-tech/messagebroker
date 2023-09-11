from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
import uuid
import datetime

class Room(Model):
    __keyspace__ = "testdb"
    id = columns.UUID(primary_key=True, default=uuid.uuid4,index=True)
    size = columns.Integer(default=2)
    created_at = columns.DateTime(required=True, default=datetime.datetime.utcnow)

    