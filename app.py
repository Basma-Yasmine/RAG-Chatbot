import chainlit as cl

from services.milvus_service import MilvusService
from services.search_service import retrieve_context
from services.llm_service import generate_answer
from services.guardrails import validate_input, validate_output

SIMILARITY_THRESHOLD = 0.35

@cl.on_chat_start
async def start():
    global milvus_service
    milvus_service = MilvusService()


@cl.on_message
async def main(message: cl.Message):

    query = message.content

    #INPUT GUARDRAILS
    valid, error = validate_input(query)

    if not valid:
        await cl.Message(content=error).send()
        return

    context, sources = retrieve_context(query, milvus_service)

    if not sources:
        await cl.Message(
            content="I don't have this information stored in my database."
        ).send()
        return

    # Check similarity score
    best_score = sources[0]["score"]

    if best_score < SIMILARITY_THRESHOLD:
        await cl.Message(
            content="I don't have this information stored in my database."
        ).send()
        return

    # Generate answer
    answer = generate_answer(query, context)

    # OUTPUT GUARDRAILS
    safe, result = validate_output(answer)

    if not safe:
        await cl.Message(content=result).send()
        return

    answer = result

    if "I don't have this information" in answer.lower():
        await cl.Message(
            content="I can't provide this information."
        ).send()
        return

    # Format retrieved chunks
    chunk_blocks = []

    for s in sources:
        block = (
            f"Chunk {s['chunk']}\n\n"
            f"{s['text']}"
        )
        chunk_blocks.append(block)

    sources_text = "\n\n---\n\n".join(chunk_blocks)

    final_response = (
        f"{answer}\n\n"
        f"Retrieved Chunks:\n\n"
        f"{sources_text}"
    )

    await cl.Message(content=final_response).send()