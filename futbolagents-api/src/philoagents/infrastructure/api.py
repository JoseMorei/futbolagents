from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from opik.integrations.langchain import OpikTracer
from pydantic import BaseModel

from philoagents.application.conversation_service.generate_response import (
    get_response,
    get_streaming_response,
)
from philoagents.application.conversation_service.reset_conversation import (
    reset_conversation_state,
)
from philoagents.domain.philosopher_factory import PlayerFactory

from .opik_utils import configure
from .telemetry import configure_telemetry

configure()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    opik_tracer = OpikTracer()
    opik_tracer.flush()


app = FastAPI(lifespan=lifespan)

configure_telemetry(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    message: str
    player_id: str


@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        player_factory = PlayerFactory()
        player = player_factory.get_player(chat_message.player_id)

        response, _ = await get_response(
            messages=chat_message.message,
            player_id=chat_message.player_id,
            player_name=player.name,
            player_perspective=player.perspective,
            player_style=player.style,
            player_context="",
        )
        return {"response": response}
    except Exception as e:
        opik_tracer = OpikTracer()
        opik_tracer.flush()

        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()

            if "message" not in data or "player_id" not in data:
                await websocket.send_json(
                    {
                        "error": "Invalid message format. Required fields: 'message' and 'player_id'"
                    }
                )
                continue

            try:
                player_factory = PlayerFactory()
                player = player_factory.get_player(data["player_id"])

                response_stream = get_streaming_response(
                    messages=data["message"],
                    player_id=data["player_id"],
                    player_name=player.name,
                    player_perspective=player.perspective,
                    player_style=player.style,
                    player_context="",
                )

                await websocket.send_json({"streaming": True})

                full_response = ""
                async for chunk in response_stream:
                    full_response += chunk
                    await websocket.send_json({"chunk": chunk})

                await websocket.send_json(
                    {"response": full_response, "streaming": False}
                )

            except Exception as e:
                opik_tracer = OpikTracer()
                opik_tracer.flush()

                await websocket.send_json({"error": str(e)})

    except WebSocketDisconnect:
        pass


@app.post("/reset-memory")
async def reset_conversation():
    try:
        result = await reset_conversation_state()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
