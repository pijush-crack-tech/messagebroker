
import json
from fastapi import WebSocket, WebSocketDisconnect
from db import get_session
from rooms.model import Room
from websocket_manager import WebSocketManager


class RoomController(WebSocketManager):

    def __init__(self):
        super().__init__()
        self.session = get_session()

    def __create_room(self,size : int) -> Room :
        room_obj = Room.objects.create(
            size = size
        )
        return room_obj

    def get_last_room(self) -> Room:
        print("gere")
        
        try:
            # data =  self.session.execute(''' SELECT * FROM room LIMIT 1''')
            data = Room.all()[-1]
            return data
        except Room.DoesNotExist:
            return None
        
    def __is_room_full(self,room_id,last_room_size):
        socket_room_length = len(self.get_room(room_id))
        print(socket_room_length,last_room_size)
        if socket_room_length == last_room_size:
            return True
        return False
    
    async def __start_game(self,room_id):
        message = {
                "room_id": str(room_id),
                "message": f"Game Started For room - {room_id}",
                "is_game_started" : True
            }
        await self.broadcast_to_room(room_id, json.dumps(message))
    
    # Create Room If not Exist and add user to that room
    async def create_or_get_last_room(self,user,websocket:WebSocket):
        message = {}
        last_room = self.get_last_room()
        if not last_room:
            last_room = self.__create_room(size=2)
        room_id = str(last_room.id)

        is_room_completed = self.__is_room_full(room_id,last_room.size)

        if is_room_completed:
            room_id = str(self.__create_room(2).id)
            message = {
                "user_id": user,
                "room_id": str(room_id),
                "message": f"User {user} connected to room - {room_id}"
            }
            await self.add_new_user_to_room(room_id,websocket,user)
        else:
            message = {
                "user_id": user,
                "room_id": room_id,
                "message": f"User {user} connected to room - {room_id}"
            }
            await self.add_new_user_to_room(str(last_room.id),websocket,user)

        await self.broadcast_to_room(room_id, json.dumps(message))

        can_start_game = self.__is_room_full(room_id,last_room.size)
        
        if can_start_game:
            await self.__start_game(room_id)

        try:
            while True:
                data = await websocket.receive_text()
                message = {
                    "user_id": user,
                    "room_id": room_id,
                    "message": data
                }
                await self.broadcast_to_room(room_id, json.dumps(message))

        except WebSocketDisconnect:
            await self.remove_user_from_room(room_id, websocket)

            message = {
                "user_id": user,
                "room_id": room_id,
                "message": f"User {user} disconnected from room - {room_id}"
            }
            await self.broadcast_to_room(room_id, json.dumps(message))
    
    
    async def add_new_user_to_room(self,room_id,websocket,user_id):
        await self.add_user_to_room(room_id, websocket,user_id)

