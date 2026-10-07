from fastapi import FastAPI, Body, Request
from gemini_client import get_answer_from_gemini
from contextlib import asynccontextmanager
from db import Base, engine, get_user_requests, add_request_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)    #создание таблиц
    yield


app = FastAPI(
    title="My project1",
    lifespan=lifespan,
    )


@app.get("/requests")
def get_my_requests(request: Request):
    user_ip_address = request.client.host
    user_requests = get_user_requests(ip_address=user_ip_address)
    return user_requests


@app.post("/requests")
def send_prompt(request: Request, prompt: str = Body(embed=True),):
    user_ip_address = request.client.host
    answer = get_answer_from_gemini(prompt)
    add_request_data(
        ip_address=user_ip_address,
        prompt=prompt,
        response=answer,
    )
    return {"answer": answer}