from pydantic import BaseModel

class CreateRoom(BaseModel):
    total_member : int


