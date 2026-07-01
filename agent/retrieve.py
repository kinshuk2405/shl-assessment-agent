import json
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from agent.domain_map import DOMAIN_MAP


TEST_TYPES = {
    "Knowledge & Skills": "K",
    "Personality & Behavior": "P",
    "Ability & Aptitude": "A",
    "Simulations": "S",
    "Assessment Exercises": "E",
    "Development & 360": "D",
    "Competencies": "C"
}


def load_catalog():

    with open("data/catalog.json", "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(item):

    test_type = "K"

    for key in item.get("keys", []):
        if key in TEST_TYPES:
            test_type = TEST_TYPES[key]
            break

    return {
        "id": item.get("entity_id"),
        "name": item.get("name"),
        "url": item.get("link"),
        "description": item.get("description", ""),
        "job_levels": item.get("job_levels", []),
        "categories": item.get("keys", []),
        "test_type": test_type
    }


def build_search_text(item):

    parts = []

    parts.append(item["name"])
    parts.append(item["description"])

    parts.extend(item["job_levels"])
    parts.extend(item["categories"])

    return " ".join(parts).lower()


def build_documents(catalog):

    docs = []

    for item in catalog:
        docs.append(
            build_search_text(item).split()
        )

    return docs



catalog = load_catalog()

catalog = [
    normalize(x)
    for x in catalog
]

print("Total assessments:", len(catalog))

documents = build_documents(catalog)

bm25 = BM25Okapi(documents)

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Creating embeddings...")

texts = [
    build_search_text(x)
    for x in catalog
]

embeddings = model.encode(
    texts,
    convert_to_tensor=True
)

print("Embeddings created.")


def semantic_search(query, top_k=10):

    q = model.encode(
        query,
        convert_to_tensor=True
    )

    scores = cos_sim(
        q,
        embeddings
    )[0]

    pairs = []

    for i, score in enumerate(scores):

        pairs.append(
            (
                float(score),
                catalog[i]
            )
        )

    pairs.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return pairs[:top_k]


def bm25_search(query, top_k=10):

    tokenized = query.lower().split()

    scores = bm25.get_scores(tokenized)

    ranked = sorted(
        zip(scores, catalog),
        key=lambda x: x[0],
        reverse=True
    )

    return ranked[:top_k]


def hybrid_search(query, top_k=10):

    scores = {}

    # BM25 contribution
    bm25_results = bm25_search(query, 20)

    for score, item in bm25_results:

        scores[item["name"]] = {
            "score": score * 0.6,
            "item": item
        }

    # Semantic contribution
    semantic_results = semantic_search(query, 20)

    for score, item in semantic_results:

        if item["name"] not in scores:
            scores[item["name"]] = {
                "score": 0,
                "item": item
            }

        scores[item["name"]]["score"] += score * 20

    # Domain boosts
    query_lower = query.lower()

    for keyword, assessments in DOMAIN_MAP.items():

        if keyword in query_lower:

            for assessment in assessments:

                for item in catalog:

                    if assessment.lower() in item["name"].lower().replace("(adaptive)", ""):

                        if item["name"] not in scores:
                            scores[item["name"]] = {
                                "score": 0,
                                "item": item
                            }

                        scores[item["name"]]["score"] += 15

    ranked = sorted(
        scores.values(),
        key=lambda x: x["score"],
        reverse=True
    )

    BLACKLIST = [
    "Interviewing and Hiring",
    "Smart Interview"
]

    filtered = []

    for item in ranked:

        bad = False

        for word in BLACKLIST:
            if word.lower() in item["item"]["name"].lower():
                bad = True
                break

        if not bad:
            filtered.append(item)

            return filtered[:top_k]

    return ranked[:top_k]


results = hybrid_search(
    "java developer who works with stakeholders"
)

print("\nHybrid Results:\n")

for result in results:

    print(f"{result['score']:.2f}")
    print(result["item"]["name"])
    print()
