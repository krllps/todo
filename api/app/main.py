from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {
        "message": "pong"
    }
