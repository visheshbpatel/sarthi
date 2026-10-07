"""UI layer for Sarthi: theme CSS and small, reusable view components.

One fixed theme, "deep lagoon": a dark blue-green page with a soft glow at the
top, pale sea-mist text, and a single champagne accent. Dark and low-glare, but
with enough depth and warmth that it doesn't read as flat.
"""

import html

import streamlit as st

ASSISTANT_AVATAR = ":material/explore:"
USER_AVATAR = ":material/person:"

# Each suggestion is a conversation starter that doubles as a capability hint.
SUGGESTIONS = [
    {"icon": ":material/calendar_month:", "title": "Schedule a meeting",
     "prompt": "Schedule a meeting for tomorrow at 3 pm"},
    {"icon": ":material/mail:", "title": "Summarize my emails",
     "prompt": "Summarize my unread emails from today"},
    {"icon": ":material/checklist:", "title": "Manage my tasks",
     "prompt": "Show my pending tasks"},
    {"icon": ":material/edit_note:", "title": "Take a quick note",
     "prompt": "Save a note: pick up groceries on the way home"},
    {"icon": ":material/payments:", "title": "Track an expense",
     "prompt": "Log an expense of ₹450 for lunch today"},
    {"icon": ":material/lightbulb:", "title": "Ask a question",
     "prompt": "Explain how vector databases work in simple terms"},
]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Cormorant+Garamond:wght@600;700&family=Noto+Serif+Devanagari:wght@600&display=swap');

:root {
    --bg: #0E1C1E;           /* deep lagoon */
    --panel: #142629;        /* cards, composer */
    --panel-hover: #1B3235;
    --line: #28434A;         /* hairlines */
    --text: #E6EFEA;         /* sea mist */
    --muted: #9DB4AE;        /* secondary text */
    --accent: #D9BC8C;       /* champagne */
    --accent-ink: #0E1C1E;
    --bubble: #1D3A3D;       /* your messages */
    --bubble-line: #30575C;
    color-scheme: dark;
}

/* Surface */
.stApp {
    background: radial-gradient(1100px 520px at 50% -8%, rgba(74, 140, 138, .20), transparent 70%) fixed, var(--bg);
    color: var(--text);
}
header[data-testid="stHeader"] { background: transparent; }
header[data-testid="stHeader"] * { color: var(--muted); }
footer, [data-testid="stDecoration"], .stAppDeployButton { display: none; }

/* Typography (scoped so Material icon fonts are left alone) */
.stApp, .stApp p, .stApp li, .stApp textarea, .stApp button {
    font-family: 'Lora', Georgia, 'Times New Roman', serif;
}
[data-testid="stMarkdownContainer"] :where(p, li, h1, h2, h3, h4, strong, em, td, th) { color: var(--text); }
[data-testid="stMarkdownContainer"] :where(p, li) { font-size: 1.12rem; line-height: 1.7; }
[data-testid="stMarkdownContainer"] a { color: var(--accent); }

/* Style-only blocks take no space in the layout */
[data-testid="stElementContainer"]:has(style):not(:has(.sarthi-title)):not(:has(.sarthi-hero)):not(:has(.sarthi-user)) { display: none; }

/* Reading column */
.stApp [data-testid="stMainBlockContainer"] {
    max-width: 740px;
    padding-top: clamp(3.5rem, 8vh, 5rem) !important;
    padding-bottom: 7rem;
}

/* Masthead */
.sarthi-title { display: flex; align-items: baseline; gap: 1rem; flex-wrap: wrap; }
.sarthi-name {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: clamp(2.5rem, 6.2vh, 3.4rem); font-weight: 700; line-height: 1.05;
    letter-spacing: .01em; color: var(--text);
}
.sarthi-script {
    font-family: 'Noto Serif Devanagari', 'Lora', serif;
    font-size: clamp(1.5rem, 3.6vh, 1.9rem); font-weight: 600; color: var(--accent);
}
.stApp .sarthi-tagline { margin: .55rem 0 0; color: var(--muted); font-size: 1.2rem; font-style: italic; }
.sarthi-rule { height: 1px; background: var(--line); margin-top: clamp(.8rem, 2vh, 1.4rem); }

/* Welcome (divs, not <h1>, so Streamlit's heading styles don't apply) */
.sarthi-hero {
    margin: clamp(1rem, 4vh, 2.4rem) 0 .4rem;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: clamp(2rem, 5.2vh, 2.9rem); font-weight: 600; line-height: 1.1; color: var(--text);
}
.stApp .sarthi-sub { margin: 0 0 clamp(.8rem, 2.2vh, 1.7rem); color: var(--muted); font-size: 1.15rem; }

/* Suggestion cards: stretch to fill each column */
[class*="st-key-suggestion_"],
[class*="st-key-suggestion_"] [data-testid="stButton"],
[class*="st-key-suggestion_"] button { width: 100% !important; }
[class*="st-key-suggestion_"] button {
    justify-content: flex-start;
    padding: clamp(.7rem, 1.9vh, 1.05rem) 1.2rem;
    border-radius: 10px;
    background: var(--panel);
    border: 1px solid var(--line);
    transition: border-color .15s ease, background-color .15s ease;
}
[class*="st-key-suggestion_"] button p { font-size: 1.12rem; font-weight: 500; color: var(--text); }
[class*="st-key-suggestion_"] button [data-testid="stIconMaterial"] { color: var(--accent); }
[class*="st-key-suggestion_"] button:hover { border-color: var(--accent); background: var(--panel-hover); }
[class*="st-key-suggestion_"] button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

/* Messages: Sarthi writes on the page, you write on a soft green card */
[data-testid="stChatMessage"] { background: transparent; padding: .8rem 0; gap: .9rem; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: var(--bubble);
    border: 1px solid var(--bubble-line);
    border-radius: 10px;
    padding: .9rem 1.2rem;
}
/* Your message text: bigger than Sarthi's replies */
.sarthi-user {
    font-size: 1.32rem; line-height: 1.55;
    color: var(--text); overflow-wrap: anywhere;
}

[data-testid="stChatMessageAvatarAssistant"] { background: var(--accent); color: var(--accent-ink); }
[data-testid="stChatMessageAvatarUser"] { background: var(--bubble-line); color: var(--text); }

/* Composer */
[data-testid="stBottom"], [data-testid="stBottom"] > div { background: var(--bg); }
[data-testid="stChatInput"] { border-radius: 12px; background: transparent; }
[data-testid="stChatInput"] > div {
    border-radius: 12px;
    border: 1px solid var(--line);
    background: var(--panel);
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 20%, transparent);
}
[data-testid="stChatInput"] textarea { color: var(--text); background: transparent; font-size: 1.1rem; }
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted); opacity: 1; }

@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def render_header() -> None:
    # Kept flat (no indentation or blank lines) so Markdown treats it as one HTML block.
    st.markdown(
        '<div class="sarthi-title">'
        '<span class="sarthi-name">Sarthi</span>'
        '<span class="sarthi-script">सारथी</span>'
        "</div>"
        '<p class="sarthi-tagline">Your personal guide and assistant</p>'
        '<div class="sarthi-rule"></div>',
        unsafe_allow_html=True,
    )


def render_welcome(on_pick) -> None:
    """Empty state: a prompt plus six starters. `on_pick(prompt)` runs on click."""
    st.markdown(
        '<div class="sarthi-hero">How may I help you today?</div>'
        '<p class="sarthi-sub">Choose a place to begin, or write your own request below.</p>',
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for i, item in enumerate(SUGGESTIONS):
        with cols[i % 2]:
            st.button(
                item["title"],
                icon=item["icon"],
                key=f"suggestion_{i}",
                on_click=on_pick,
                args=(item["prompt"],),
            )


def bubble(role: str):
    """Chat message container with Sarthi's avatars."""
    avatar = ASSISTANT_AVATAR if role == "assistant" else USER_AVATAR
    return st.chat_message(role, avatar=avatar)


def render_message(message: dict) -> None:
    with bubble(message["role"]):
        if message.get("error"):
            st.error(message["content"], icon=":material/error:")
        elif message["role"] == "user":
            # Escaped and kept on one line so Markdown treats it as a single HTML block.
            text = html.escape(message["content"]).replace("\n", "<br>")
            st.markdown(f'<div class="sarthi-user">{text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(message["content"])


def lock_scroll() -> None:
    """Welcome screen only: no scrollbar on screens tall enough to fit it.

    Not called once the chat starts, so scrolling comes back automatically.
    """
    st.markdown(
        "<style>@media (min-height: 700px) {"
        "[data-testid='stMain'], .stMain, section.main { overflow-y: hidden !important; }"
        ".stApp [data-testid='stMainBlockContainer'] { padding-bottom: 1rem !important; }"
        "}</style>",
        unsafe_allow_html=True,
    )