def classify(messages, state):

    last_user = ""

    for msg in reversed(messages):

        if msg["role"] == "user":
            last_user = msg["content"].lower()
            break

    # prompt injection
    if any(
        x in last_user
        for x in [
            "ignore previous instructions",
            "system prompt",
            "jailbreak",
            "developer prompt"
        ]
    ):
        return "REFUSE"

    # out of scope
    if any(
        x in last_user
        for x in [
            "legal advice",
            "salary negotiation",
            "employment law",
            "hiring strategy"
        ]
    ):
        return "REFUSE"

    # comparison
    if state["compare"]:
        return "COMPARE"

    # refinement
    if (
        "add" in last_user
        or "include" in last_user
        or "also" in last_user
        or "instead" in last_user
    ):
        return "REFINE"

    # clarification
    if state["role"] is None:
        return "CLARIFY"

    if state["experience"] is None:
        return "CLARIFY"

    # recommend
    return "RECOMMEND"

if __name__ == "__main__":
    
    try:
        from agent.state import reconstruct
    except:
        from state import reconstruct

    messages = [

        {
            "role":"user",
            "content":"Hiring a Java developer"
        },

        {
            "role":"assistant",
            "content":"What seniority?"
        },

        {
            "role":"user",
            "content":"4 years experience"
        },

        {
            "role":"user",
            "content":"Add personality tests"
        }
    ]

    state = reconstruct(messages)

    print(state)

    print()

    print(
        classify(messages, state)
    )