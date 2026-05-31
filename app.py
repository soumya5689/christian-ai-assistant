
import streamlit as st
from backend.image.image_generator import generate_image

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Christian AI Assistant",
    page_icon="✝️",
    layout="wide"
)

# =====================================
# LOAD BACKEND
# =====================================

@st.cache_resource
def load_backend():

    from backend.chat_service import (
        handle_user_query
    )

    return handle_user_query

handle_user_query = load_backend()

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.main {
    padding-top: 0.5rem;
}

.big-title {
    text-align:center;
    font-size:42px;
    font-weight:bold;
}

.sub-title {
    text-align:center;
    color:#A0A0A0;
    margin-bottom:20px;
}

.metric-box {
    padding:10px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================
# HEADER
# =====================================

st.markdown(
    """
    <div class='big-title'>
        ✝️ Christian AI Assistant
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='sub-title'>
        Scripture Grounded • Safe • Denomination Aware
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.header("⚙ Settings")

    denomination = st.selectbox(
        "Choose Denomination",
        [
            "Neutral",
            "Catholic",
            "Protestant",
            "Orthodox"
        ]
    )

    st.divider()

    st.subheader("📊 Statistics")

    st.metric(
        "📖 Bible Verses",
        "31,100"
    )

    st.metric(
        "💬 Session Messages",
        len(st.session_state.messages)
    )

    st.metric(
        "🧠 Memory",
        "Enabled"
    )

    st.divider()

    st.subheader("✨ Features")

    st.markdown("""
    ✅ Scripture Verification

    ✅ Bible Grounding

    ✅ Safety Moderation

    ✅ Conversation Memory

    ✅ Denomination Support

    ✅ Christian Image Generation
    """)

# =====================================
# TABS
# =====================================

chat_tab, image_tab, about_tab = st.tabs(
    [
        "💬 Chat Assistant",
        "🎨 Image Studio",
        "ℹ️ About"
    ]
)

# =====================================
# CHAT TAB
# =====================================

with chat_tab:

    st.markdown("### Quick Questions")

    col1, col2 = st.columns(2)

    quick_prompt = None

    with col1:

        if st.button(
            "🙏 What is Salvation?"
        ):
            quick_prompt = (
                "What is salvation?"
            )

        if st.button(
            "📖 Explain John 3:16"
        ):
            quick_prompt = (
                "Explain John 3:16"
            )

    with col2:

        if st.button(
            "❤️ What is Forgiveness?"
        ):
            quick_prompt = (
                "What does the Bible say about forgiveness?"
            )

        if st.button(
            "🙏 How should Christians pray?"
        ):
            quick_prompt = (
                "How should Christians pray?"
            )

    st.divider()

    for msg in st.session_state.messages:

        with st.chat_message(
            msg["role"]
        ):

            st.markdown(
                msg["content"]
            )

    user_prompt = st.chat_input(
        "Ask a Christian question..."
    )

    if quick_prompt:
        user_prompt = quick_prompt

    if user_prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.spinner(
            "Searching scripture..."
        ):

            response = handle_user_query(
                user_prompt,
                denomination
            )

        with st.chat_message(
            "assistant"
        ):

            st.markdown(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

# ====================================
# IMAGE TAB
# ====================================

with image_tab:

    import requests
    from PIL import Image
    from io import BytesIO

    st.subheader(
        "🎨 Christian Image Studio"
    )

    style = st.selectbox(
        "Art Style",
        [
            "Realistic",
            "Biblical Painting",
            "Cinematic",
            "Watercolor",
            "Ancient Jerusalem"
        ]
    )

    image_prompt = st.text_area(
        "Describe the image",
        placeholder=
        "Jesus teaching disciples beside a lake"
    )

    if st.button(
        "Generate Christian Artwork"
    ):

        if image_prompt.strip():

            try:

                full_prompt = (
                    f"{style}. "
                    f"Christian artwork. "
                    f"{image_prompt}"
                )

                image_url = generate_image(
                    full_prompt
                )

                with st.spinner(
                    "Generating image..."
                ):

                    response = requests.get(
                        image_url,
                        timeout=60
                    )

                    image = Image.open(
                        BytesIO(
                            response.content
                        )
                    )

                    st.image(
                        image,
                        caption=
                        "Generated Christian Artwork",
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    f"Image generation failed: {e}"
                )

                st.markdown(
                    f"[Open Image Directly]({image_url})"
                )

        else:

            st.warning(
                "Please enter an image description."
            )
# =====================================
# ABOUT TAB
# =====================================

with about_tab:

    st.markdown("""
## Christian AI Assistant

An AI-powered Christian assistant built using:

- Gemini
- ChromaDB
- Sentence Transformers
- Streamlit

### Core Features

- Scripture Grounded Responses
- Bible Verse Verification
- Denomination Awareness
- Conversation Memory
- Safety Moderation
- Christian Image Generation

### Architecture

User
↓
Streamlit UI
↓
Safety Layer
↓
Scripture Verification
↓
Bible RAG Search
↓
ChromaDB
↓
Gemini
↓
Response

### Dataset

King James Version (KJV)

31,100 Bible verses indexed in ChromaDB.
""")
