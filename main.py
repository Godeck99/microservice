from fastapi import FastAPI

app = FastAPI(title="FastAPI Locust")


@app.get("/cpu_intensive")
async def cpu_intensive(n: int = 30):
    def fib(n):
        if n in (0, 1):
            return n
        return fib(n - 1) + fib(n - 2)

    return {"result": fib(n)}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
