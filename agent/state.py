import re


def reconstruct(messages):

    state = {
        "role": None,
        "experience": None,
        "personality": False,
        "stakeholder": False,
        "compare": [],
        "query": ""
    }

    for msg in messages:

        if msg["role"] != "user":
            continue

        text = msg["content"].lower()

        state["query"] += " " + text

        # experience
        years = re.findall(r"\d+", text)

        if years:
            state["experience"] = int(years[0])

        # role extraction
        if "java" in text:
            state["role"] = "java developer"

        elif "python" in text:
            state["role"] = "python developer"

        elif "data scientist" in text:
            state["role"] = "data scientist"

        elif "developer" in text:
            state["role"] = "developer"

        # personality
        if "personality" in text:
            state["personality"] = True

        # stakeholder
        if "stakeholder" in text:
            state["stakeholder"] = True

        if "stakeholders" in text:
            state["stakeholder"] = True

        # comparison
        if " vs " in text:
            state["compare"].append(text)

        if "difference" in text:
            state["compare"].append(text)

    return state

if __name__ == "__main__":

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
            "content":"Works with stakeholders"
        },

        {
            "role":"user",
            "content":"Add personality tests"
        }
    ]

    print(
        reconstruct(messages)
    )