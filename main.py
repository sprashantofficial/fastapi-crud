from fastapi import FastAPI

app = FastAPI(title="Task API")


@app.get("/")
def home():
    return {"message": "Hello, World!"}
