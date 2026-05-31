from backend.moderation.safety import is_safe

from backend.verifier.scripture_verifier import (
    parse_reference,
    get_verse
)

from backend.rag.search_bible import (
    search_bible
)

from backend.memory.memory import (
    ConversationMemory
)

from backend.llm.gemini_client import (
    generate_answer
)

from backend.prompts.denomination import (
    DENOMINATION_PROMPTS
)


memory = ConversationMemory()

FOLLOW_UP_PHRASES = [
    "explain further",
    "tell me more",
    "can you explain",
    "more detail",
    "elaborate",
    "what do you mean",
    "explain that"
]


def build_context(results):

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    context = []

    for doc, meta in zip(
        docs,
        metas
    ):

        context.append(
            f"{meta['book']} "
            f"{meta['chapter']}:{meta['verse']}\n"
            f"{doc}"
        )

    return "\n\n".join(context)


def handle_user_query(
    user_input,
    denomination="Neutral"
):

    # --------------------
    # Save User Message
    # --------------------

    memory.add_message(
        "user",
        user_input
    )

    # --------------------
    # Safety Check
    # --------------------

    safe, reason = is_safe(
        user_input
    )

    if not safe:

        return f"❌ {reason}"

    # --------------------
    # Verse Lookup
    # --------------------

    parsed = parse_reference(
        user_input
    )

    if parsed:

        book, chapter, verse = parsed

        result = get_verse(
            book,
            chapter,
            verse
        )

        if result:

            response = (
                f"{result['book']} "
                f"{result['chapter']}:"
                f"{result['verse']}\n\n"
                f"{result['text']}"
            )

            memory.add_message(
                "assistant",
                response
            )

            return response

        return "Verse not found."

    # --------------------
    # Follow-up Detection
    # --------------------

    query_for_search = user_input

    lower_input = user_input.lower()

    if any(
        phrase in lower_input
        for phrase in FOLLOW_UP_PHRASES
    ):

        previous_question = (
            memory.get_last_user_message()
        )

        if previous_question:

            query_for_search = (
                previous_question
            )

    # --------------------
    # Bible Search
    # --------------------

    search_results = search_bible(
        query_for_search
    )

    bible_context = build_context(
        search_results
    )

    denomination_prompt = (
        DENOMINATION_PROMPTS.get(
            denomination,
            DENOMINATION_PROMPTS["Neutral"]
        )
    )

    history = memory.get_history()

    answer = generate_answer(
        question=user_input,
        bible_context=bible_context,
        denomination_prompt=denomination_prompt,
        history=str(history)
    )

    memory.add_message(
        "assistant",
        answer
    )

    return answer


if __name__ == "__main__":

    print("\nChristian AI Assistant\n")

    denomination = input(
        "Choose denomination "
        "(Neutral/Catholic/Protestant/Orthodox): "
    )

    while True:

        user_input = input(
            "\nAsk: "
        )

        response = handle_user_query(
            user_input,
            denomination
        )

        print("\nResponse:\n")

        print(response)