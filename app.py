import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))  # Pega a porta do Render
    uvicorn.run(app, host="0.0.0.0", port=port)  # Escuta na porta correta
