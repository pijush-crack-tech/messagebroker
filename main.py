

import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from rooms.controller import RoomController

from rooms.model import Room
from user.models import User
from fastapi.middleware.cors import CORSMiddleware

from user.views import router
from rooms.views import room_router
from cassandra.cqlengine.management import sync_table
import db
from websocket_manager import WebSocketManager

app = FastAPI()
all_db_models = [User,Room]

app.include_router(router,tags=["data"])
app.include_router(room_router,tags=["room"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    global session
    session = db.get_session()
    for model in all_db_models:
        try:
            sync_table(model)
        except:
            pass


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/home")
async def get():
    return HTMLResponse(html)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# socket_manager = WebSocketManager()
room_controller = RoomController()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):

    await room_controller.create_or_get_last_room(user_id,websocket)
