from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List

router = APIRouter(
    tags=["Chat"]
)

# ── Connection Manager ─────────────────────────────────
class ConnectionManager:
    def __init__(self):
        # Dictionary: project_id → list of connected websockets
        # Example: { 1: [ws1, ws2], 2: [ws3] }
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, project_id: int, websocket: WebSocket):
        # Accept the incoming WebSocket connection
        await websocket.accept()

        # If this project has no room yet → create one
        if project_id not in self.active_connections:
            self.active_connections[project_id] = []

        # Add this connection to the project's room
        self.active_connections[project_id].append(websocket)

    def disconnect(self, project_id: int, websocket: WebSocket):
        # Remove this connection from the project's room
        self.active_connections[project_id].remove(websocket)

    async def broadcast(self, project_id: int, message: str):
        # Send message to EVERYONE in this project's room
        # Loop through all connections in this room
        if project_id in self.active_connections:
            for connection in self.active_connections[project_id]:
                await connection.send_text(message)


# Create ONE manager instance — shared across all connections
manager = ConnectionManager()


# ── WebSocket Endpoint ─────────────────────────────────
@router.websocket("/ws/{project_id}/{username}")
async def websocket_chat(
    project_id: int,
    username: str,
    websocket: WebSocket
):
    # Step 1: Connect this user to the project's room
    await manager.connect(project_id, websocket)

    # Announce to everyone that this user joined
    await manager.broadcast(
        project_id,
        f"🟢 {username} joined the room"
    )

    try:
        # Step 2: Keep listening for messages
        while True:
            # Wait for this user to send a message
            message = await websocket.receive_text()

            # Broadcast it to everyone in the room
            await manager.broadcast(
                project_id,
                f"{username}: {message}"
            )

    except WebSocketDisconnect:
        # Step 3: User disconnected (closed tab, lost internet etc)
        manager.disconnect(project_id, websocket)

        # Announce to everyone that this user left
        await manager.broadcast(
            project_id,
            f"🔴 {username} left the room"
        )