from fastapi import FastAPI, Request
from fastapi.responses import Response
import httpx

app = FastAPI()


@app.get("/route1")
async def route1():
    return {"message": "This is route 1"}


@app.get("/route2")
async def route2():
    return {"message": "This is route 2"}


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    url = f"http://localhost:5001/{path}"
    headers = dict(request.headers)

    data = await request.body()

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            response = await client.get(url, headers=headers)
        elif request.method == "POST":
            response = await client.post(url, headers=headers, content=data)
        elif request.method == "PUT":
            response = await client.put(url, headers=headers, content=data)
        elif request.method == "DELETE":
            response = await client.delete(url, headers=headers, content=data)

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
