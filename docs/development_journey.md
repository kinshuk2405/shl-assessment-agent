# SHL Conversational Assessment Recommender

## Development Journey

### Project Goal

Build a stateless conversational agent capable of recommending SHL Individual Test Solutions through dialogue. The agent should clarify ambiguous requests, refine recommendations based on user feedback, compare assessments using catalog-grounded information, and remain strictly within the SHL assessment domain.

---

## Hour 1: Project Setup and Architecture Planning

### Objective

Establish the project structure and understand the assignment requirements.

### Activities

- Read the assignment specification thoroughly.
- Identified the four required conversational behaviors:
  - Clarification
  - Recommendation
  - Refinement
  - Comparison

- Analyzed evaluation criteria:
  - Schema compliance
  - Recall@10
  - Behavioral probes

- Decided to implement a stateless architecture because the evaluator provides complete conversation history in every API request.

### Design Decisions

- Selected **FastAPI** due to:
  - Native JSON schema validation
  - Automatic OpenAPI documentation
  - Lightweight deployment

- Chose a modular project structure separating:
  - Retrieval
  - State reconstruction
  - Intent detection
  - Comparison
  - Guardrails

### Deliverables

- Created Python virtual environment.
- Installed project dependencies.
- Created project folder structure.
- Implemented initial FastAPI skeleton.
- Implemented `/health` endpoint.
- Implemented `/chat` endpoint.

---

## Hour 2: SHL Catalog Exploration and Data Modeling

### Objective

Understand and structure the SHL assessment catalog.

### Activities

- Explored the provided SHL catalog JSON.
- Identified approximately 377 Individual Test Solutions.
- Verified the presence of key assessments including:
  - OPQ32r
  - Verify General Ability Screen
  - Business Communications
  - Automata
  - Java assessments

### Design Decisions

- Decided against using a vector database because:
  - The catalog size is small enough to fit entirely in memory.
  - Fast retrieval can be achieved using hybrid search techniques.

- Created a normalization layer to standardize catalog entries.

### Deliverables

- Implemented catalog loader.
- Implemented catalog normalization.
- Implemented test type mapping.

---

## Hour 3: Lexical Retrieval Using BM25

### Objective

Build a baseline retrieval system.

### Activities

- Implemented BM25 indexing using rank-bm25.
- Constructed searchable documents by combining:
  - Assessment name
  - Description
  - Job levels
  - Categories

### Findings

BM25 performed well for explicit technical requirements such as:

- Java
- SQL
- Programming skills

However, BM25 struggled with behavioral requirements.

### Deliverables

- BM25 indexing pipeline.
- BM25 search functionality.
- Initial recommendation ranking.

---

## Hour 4: Semantic Retrieval

### Objective

Improve retrieval quality using embeddings.

### Activities

- Implemented Sentence Transformers using:
  - `all-MiniLM-L6-v2`

- Generated embeddings for all assessments.
- Implemented cosine similarity search.

### Findings

Semantic retrieval improved concept matching but still failed to retrieve behavioral assessments consistently.

Example:
Query:

> "Java developer who works with stakeholders"

Results:

- Java assessments ranked highly.
- Personality and communication assessments were not adequately retrieved.

### Deliverables

- Embedding generation pipeline.
- Semantic search implementation.

---

## Hour 5: Hybrid Retrieval and Domain Knowledge Layer

### Objective

Improve Recall@10 through retrieval fusion.

### Activities

Implemented a three-stage retrieval architecture:

1. BM25 lexical retrieval
2. Semantic retrieval
3. Domain-specific boosting

Created a domain mapping layer linking behavioral concepts to known SHL assessments.

Examples:

- stakeholder → OPQ32r, Business Communications, Verify General Ability Screen
- personality → OPQ32r
- developer → Automata
- java → Java assessments

### Findings

Domain-aware boosting significantly improved retrieval quality.

Example:
Query:

> "Hiring a Java developer who works with stakeholders"

Retrieved assessments:

- Java 8 (New)
- Core Java (Advanced Level)
- Business Communications
- Business Communication (adaptive)
- Occupational Personality Questionnaire OPQ32r
- Verify General Ability Screen
- Automata

### Conclusion

Hybrid retrieval substantially improved expected Recall@10 compared to either BM25 or semantic retrieval alone.

---

## Current Architecture

```text
Conversation History
          ↓
State Reconstruction
          ↓
Intent Detection
          ↓
Hybrid Retrieval
          ├── BM25
          ├── Semantic Search
          └── Domain Boosting
          ↓
Recommendation Engine
          ↓
FastAPI Response
```

---

## Key Lessons Learned

- Small, domain-specific datasets benefit more from hybrid retrieval than from pure semantic search.
- Behavioral and personality requirements require explicit domain knowledge.
- Stateless agent architectures simplify deployment and evaluation.
- Recall-oriented retrieval is more important than generative sophistication for recommendation tasks.

---

## Future Improvements

- Add structured comparison between assessments.
- Improve state reconstruction using lightweight NLP.
- Introduce reranking for final recommendation ordering.
- Add evaluation harness against public conversation traces.

---

## Hour 6

### Conversation State Reconstruction

Implemented a stateless state reconstruction layer.

Features extracted:

- Role
- Experience
- Personality requirements
- Stakeholder interaction requirements
- Comparison requests

Rationale:
Since the evaluator sends complete conversation history on every request, maintaining server-side conversation state is unnecessary and potentially harmful.

Example:

Conversation:

- Hiring a Java developer
- 4 years experience
- Works with stakeholders
- Add personality tests

Reconstructed state:
{
role: "java developer",
experience: 4,
stakeholder: true,
personality: true
}

---

## Hour 7: Intent Classification and Conversational Behavior Design

### Objective

Implement deterministic conversational behavior handling.

### Activities

Designed a rule-based intent classification system supporting the required conversational behaviors:

- Clarify
- Recommend
- Refine
- Compare
- Refuse

Implemented intent detection using reconstructed conversation state and the latest user utterance.

### Design Decisions

Chose rule-based intent classification over LLM-based routing because:

- The evaluator imposes strict turn limits.
- Deterministic behavior improves reliability.
- Rule-based classification is easier to debug and evaluate.

### Example Behaviors

Input:

> "I need an assessment"

Output:

> CLARIFY

Input:

> "Add personality tests"

Output:

> REFINE

Input:

> "What is the difference between OPQ and GSA?"

Output:

> COMPARE

Input:

> "Ignore previous instructions"

Output:

> REFUSE

### Deliverables

- Intent classification engine
- Prompt-injection detection
- Out-of-scope request detection

---

## Hour 8: FastAPI Integration and Stateless Agent Construction

### Objective

Integrate retrieval, state reconstruction, and intent classification into a single API service.

### Activities

Integrated the following components:

- State reconstruction
- Intent classification
- Hybrid retrieval
- Recommendation formatting
- Comparison engine
- Guardrail handling

Implemented the required API endpoints:

- `GET /health`
- `POST /chat`

### Design Decisions

Maintained a fully stateless architecture by reconstructing conversation context from the complete message history included in every request.

### Deliverables

- End-to-end conversational recommendation pipeline
- Schema-compliant API responses
- Structured recommendation output

---

## Hour 9: Comparison Engine and Retrieval Refinement

### Objective

Implement catalog-grounded assessment comparison and improve recommendation quality.

### Activities

Implemented comparison support for SHL assessments using catalog metadata.

Example:

> "What is the difference between OPQ and GSA?"

Implemented a hybrid retrieval ranking approach combining:

- BM25 lexical retrieval
- Sentence-transformer semantic retrieval
- Domain-specific boosting

Refined domain mappings for:

- Personality assessments
- Communication assessments
- Cognitive assessments
- Technical assessments

### Findings

Pure semantic retrieval was insufficient for behavioral requirements.

Introducing domain-specific boosting significantly improved recommendation quality and expected Recall@10.

### Deliverables

- Comparison module
- Improved recommendation ranking
- Domain knowledge enhancement layer

---

## Hour 10: Testing, Debugging, and Stabilization

### Objective

Validate all required conversational behaviors and improve system robustness.

### Activities

Performed end-to-end testing for:

- Clarification
- Recommendation
- Refinement
- Comparison
- Refusal handling

Debugging tasks included:

- Resolving Python package import issues
- Correcting domain mappings to match catalog entries
- Improving hybrid retrieval ranking
- Stabilizing FastAPI responses
- Adding exception handling to prevent API failures

### Final Supported Behaviors

✓ Clarify vague requests

✓ Recommend SHL assessments

✓ Refine recommendations using updated constraints

✓ Compare assessments using catalog data

✓ Refuse out-of-scope and prompt-injection requests

### Final Architecture

```text
Conversation History
          ↓
State Reconstruction
          ↓
Intent Classification
          ↓
Hybrid Retrieval
          ├── BM25
          ├── Semantic Search
          └── Domain Knowledge Boosting
          ↓
Recommendation Engine
          ↓
FastAPI Response
```

### Conclusion

The final system combines deterministic conversational control with hybrid retrieval techniques to maximize recommendation quality while ensuring strict adherence to the SHL assessment catalog and evaluation constraints.
