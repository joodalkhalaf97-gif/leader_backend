from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import websocket_manager
router = APIRouter()

@router.websocket("/ws/notifications/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            # ننتظر هنا لإبقاء الاتصال مفتوحاً
            data = await websocket.receive_text() 
    except WebSocketDisconnect:
        manager.disconnect(user_id)