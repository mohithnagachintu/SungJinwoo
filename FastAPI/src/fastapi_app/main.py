from fastapi_app.app import create_app
import uvicorn

app = create_app()

def run() -> None:
    uvicorn.run("fastapi_app.main:app",
                host = "127.0.0.1",
                port = 8000,
                reload = True
    )

