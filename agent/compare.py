from agent.retrieve import catalog


def compare(a, b):

    aliases = {
        "opq": "Occupational Personality Questionnaire OPQ32r",
        "gsa": "Verify - General Ability Screen",
        "verify": "Verify - General Ability Screen"
    }

    a = aliases.get(a.lower(), a)
    b = aliases.get(b.lower(), b)

    first = None
    second = None

    for item in catalog:

        if item["name"] == a:
            first = item

        if item["name"] == b:
            second = item

    if not first or not second:
        return "Unable to compare assessments."

    return (
        f"{first['name']} is a "
        f"{first['test_type']} assessment focused on personality and behavioral traits, "
        f"whereas "
        f"{second['name']} is a "
        f"{second['test_type']} assessment focused on cognitive ability and aptitude."
    )