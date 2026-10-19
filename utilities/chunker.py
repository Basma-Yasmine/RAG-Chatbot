def split_text(text, chunk_size=500):
    """
    Splits text into chunks of approximately chunk_size characters,
    preserving sentence boundaries.
    """

    sentences = text.replace("\n", " ").split(". ")

    chunks = []
    current_chunk = ""
    
    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        sentence += "."

        if len(current_chunk) + len(sentence) <= chunk_size:

            current_chunk += sentence + " "

        else:

            chunks.append(current_chunk.strip())

            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
