from fastapi import FastAPI
import uvicorn


app = FastAPI(title="Play with Postgres", openapi_url="/openapi.json")


@app.get("/")
async def index():
    return {"Health": "OK!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, access_log=True)
