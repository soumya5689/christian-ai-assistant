

import sys

BLOCKED_PATTERNS = [
    "rewrite bible",
    "support racism",
    "support genocide",
    "religious hate",
    "hate group",
    "kill unbelievers",
    "fake scripture",
    "invent bible verse",
    "create a bible verse",
    "justify slavery",
    "justify violence",
]


def is_safe(user_input: str):
    text = (user_input or "").lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in text:
            return False, f"Blocked pattern: {pattern}"

    return True, "Safe"


if __name__ == "__main__":
    try:
        # If stdin is not a TTY (non-interactive), run a small smoke test
        if not sys.stdin.isatty():
            print("Non-interactive mode detected — running smoke tests.")
            samples = [
                "Please rewrite bible John 3:16",
                "Tell me about love",
                "Justify slavery",
            ]
            for s in samples:
                safe, reason = is_safe(s)
                print(f"Input: {s}\nSafe: {safe} Reason: {reason}\n")
            sys.exit(0)

        print("Safety checker interactive mode. Press Ctrl+C to exit.")

        while True:
            # Print prompt and flush to ensure visibility in all terminals
            print("\nEnter prompt: ", end="", flush=True)
            try:
                user_input = input()
            except EOFError:
                print("\nEOF received — exiting.")
                break

            safe, reason = is_safe(user_input)
            print(safe, reason)

    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")