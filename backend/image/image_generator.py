import urllib.parse

def generate_image(prompt):

    full_prompt = (
        "Christian biblical artwork, "
        + prompt
    )

    encoded = urllib.parse.quote(
        full_prompt
    )

    return (
        f"https://image.pollinations.ai/prompt/{encoded}"
    )