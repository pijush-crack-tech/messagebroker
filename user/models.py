from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
import uuid
import datetime

class User(Model):
    __keyspace__ = "testdb"

    id = columns.UUID(primary_key=True, default=uuid.uuid4,index=True)
    name = columns.Text(required = True)
    mobile = columns.Text(required = True)
    # room_id=columns.UUID(required=True,partition_key=True) 
    # room_name=columns.Text(required=True)
    # from_user_idname=columns.Text(required=True,index=True)
    # to_user_idname=columns.Text(required=True,index=True)
    # created_at = columns.DateTime(required=True, default=datetime.datetime.utcnow)
    # status=columns.Text(default='pending') #accepted, rejected
    # is_private_room=columns.Boolean(required=True,index=True)