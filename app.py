from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from agent.state import reconstruct
from agent.intent import classify
from agent.retrieve import hybrid_search

app = FastAPI()

import os

PORT = int(os.environ.get("PORT", 7860))  

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str


class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    messages = [
        x.dict()
        for x in request.messages
    ]

    state = reconstruct(messages)

    intent = classify(
        messages,
        state
    )


    # REFUSE
    if intent == "REFUSE":

        return ChatResponse(
            reply="I can only assist with SHL assessments.",
            recommendations=[],
            end_of_conversation=True
        )

    # CLARIFY
    if intent == "CLARIFY":

        if state["role"] is None:

            return ChatResponse(
                reply="What role are you hiring for?",
                recommendations=[],
                end_of_conversation=False
            )

        return ChatResponse(
            reply="What is the seniority or experience level?",
            recommendations=[],
            end_of_conversation=False
        )

    # COMPARE
    if intent == "COMPARE":

        from agent.compare import compare

        reply = compare(
        "OPQ",
        "GSA"
        )

        return ChatResponse(
            reply=reply,
            recommendations=[],
            end_of_conversation=False
        )

    # RECOMMEND / REFINE
    results = hybrid_search(
        state["query"]
    )

    recommendations = []

    for result in results:

        item = result["item"]

        recommendations.append(
            Recommendation(
                name=item["name"],
                url=item["url"],
                test_type=item["test_type"]
            )
        )

    return ChatResponse(
        reply=f"Here are {len(recommendations)} recommended assessments.",
        recommendations=recommendations,
        end_of_conversation=False
    )


@app.get("/")
def root():
    return {
        "message": "SHL Conversational Assessment Recommender"
    }
