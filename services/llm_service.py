from openai import OpenAI
from config import OPENAI_API_KEY, LLM_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(query, context, history=None):
    conversation = ""
    if history:
        for turn in history[-4:]: 
            conversation += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"

    prompt = f"""
You are a document assistant.

STRICT RULES:
- Answer ONLY using the provided context.
- If the answer is not present in the context, reply exactly with:
"I don't have this information stored in my database."
- Do not use outside knowledge.
- Do not guess.

Conversation so far:
{conversation}

Context:
{context}

Question:
{query}

Answer:
"""
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You answer only from the given context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content