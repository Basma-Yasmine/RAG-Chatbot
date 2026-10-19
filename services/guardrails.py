RESTRICTED_KEYWORDS = ["api_key", "password", "secret", "system prompt"]

def validate_input(user_input):
    for kw in RESTRICTED_KEYWORDS:
        if kw.lower() in user_input.lower():
            return False, f"Input contains restricted keyword: {kw}"
    if len(user_input.strip()) == 0:
        return False, "Input cannot be empty."
    return True, None


def validate_output(llm_output):
    for kw in RESTRICTED_KEYWORDS:
        if kw.lower() in llm_output.lower():
            return False, "Output blocked due to sensitive content."
    return True, llm_output