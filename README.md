# SHL Conversational Assessment Recommender

## Overview

This project implements a stateless conversational recommendation agent for SHL Individual Test Solutions.

The agent supports:

- Clarification of vague hiring requests
- Recommendation of SHL assessments
- Refinement of recommendations based on updated requirements
- Comparison of SHL assessments
- Refusal of out-of-scope requests and prompt injection attempts

The system is designed to satisfy the requirements specified in the SHL AI Intern take-home assignment.

---

## Architecture

```text
Conversation History
          ↓
State Reconstruction
          ↓
Intent Classification
          ↓
Hybrid Retrieval
          ├── BM25
          ├── Semantic Retrieval
          └── Domain Knowledge Boosting
          ↓
Recommendation Engine
          ↓
FastAPI Response
```

---

## Retrieval Strategy

The recommendation engine uses a hybrid retrieval approach:

### 1. BM25 Retrieval

- Captures explicit technical requirements
- Strong performance on skills and technologies

### 2. Semantic Retrieval

- Uses Sentence Transformers
- Model:
  - all-MiniLM-L6-v2

### 3. Domain Knowledge Boosting

- Injects SHL-specific behavioral and personality knowledge
- Improves Recall@10 for behavioral requirements

---

## Conversational Behaviors Supported

### Clarify

Example:

> "I need an assessment"

Response:

> "What role are you hiring for?"

---

### Recommend

Example:

> "Hiring a Java developer with 4 years experience"

Returns a structured shortlist of SHL assessments.

---

### Refine

Example:

> "Add personality tests"

Updates recommendations without restarting the conversation.

---

### Compare

Example:

> "What is the difference between OPQ and GSA?"

Returns a catalog-grounded comparison.

---

### Refuse

Refuses:

- Prompt injection attempts
- Legal advice
- Hiring strategy questions
- Non-SHL requests

---

## API

### GET /health

Returns:

```json
{
  "status": "ok"
}
```

---

### POST /chat

Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer"
    }
  ]
}
```

Response:

```json
{
  "reply": "...",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
uvicorn app:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Tech Stack

- Python
- FastAPI
- Sentence Transformers
- rank-bm25
- Pydantic
- Uvicorn

---

## Design Decisions

- Stateless architecture
- Hybrid retrieval instead of vector databases
- Rule-based intent classification
- Domain-specific retrieval enhancement
- Catalog-grounded comparison

---

## Future Improvements

- Learning-to-rank reranking
- More sophisticated comparison generation
- Evaluation harness using public traces
- Improved role extraction using lightweight NLP
