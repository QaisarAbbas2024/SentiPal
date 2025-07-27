import streamlit as st
from transformers import pipeline
import random
from streamlit.components.v1 import html

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="SentiPal - Emotional AI Companion",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------- Enhanced CSS -----------------
st.markdown("""
<style>
html, body {
    height: 100%;
    overflow-x: hidden;
}
.stApp {
    background: linear-gradient(135deg, #ff9a9e 0%, #c90076 100%) !important;
}
.chat-container {
    position: fixed;
    bottom: 100px;
    right: 20px;
    width: 350px;
    max-height: 500px;
    overflow-y: auto;
    background: white;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    padding: 15px;
    z-index: 100;
    display: none;
    animation: fadeIn 0.3s;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.chat-visible { display: block !important; }
.user-message {
    background: #ffffff;
    border-radius: 15px 15px 0 15px;
    padding: 12px 16px;
    margin: 10px 0;
    margin-left: auto;
    max-width: 80%;
    word-wrap: break-word;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.bot-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 15px 15px 15px 0;
    padding: 12px 16px;
    margin: 10px 0;
    margin-right: auto;
    max-width: 80%;
    word-wrap: break-word;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.stTextInput>div>div>input {
    border-radius: 25px !important;
    padding: 14px !important;
    font-size: 16px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    border: 1px solid #ff9a9e !important;
}
.stButton>button {
    border-radius: 25px !important;
    padding: 12px 24px !important;
    transition: all 0.3s !important;
    margin: 8px !important;
    font-weight: bold !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 8px rgba(0,0,0,0.15) !important;
}
.fun-button {
    background: linear-gradient(45deg, #FF9A8B, #FF6B95) !important;
    color: white !important;
}
.advice-button {
    background: linear-gradient(45deg, #4FACFE, #00F2FE) !important;
    color: white !important;
}
.game-button {
    background: linear-gradient(45deg, #6A11CB, #2575FC) !important;
    color: white !important;
}
.celebration-button {
    background: linear-gradient(45deg, #FFC312, #EE5A24) !important;
    color: white !important;
}
.close-chat-btn {
    background: linear-gradient(45deg, #ff6b6b, #ff8e8e) !important;
    color: white !important;
    width: 100%;
    margin-top: 15px !important;
    font-weight: bold !important;
}
.title-text {
    color: #ffffff;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}
/* Animation container styles */
.celebration-container {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    pointer-events: none !important;
    z-index: 9999 !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------- Celebration Effects -----------------
def show_confetti():
    # Simple confetti that works in Hugging Face Spaces
    confetti_js = """
    <script>
    (function() {
        const container = document.createElement('div');
        container.className = 'celebration-container';
        document.body.appendChild(container);
        
        const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff'];
        const emojis = ['✨', '🌟', '🎉'];
        
        for (let i = 0; i < 100; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.style.position = 'absolute';
                confetti.style.width = '15px';
                confetti.style.height = '15px';
                confetti.style.left = Math.random() * 100 + 'vw';
                confetti.style.top = '-20px';
                
                if (Math.random() > 0.7) {
                    // Emoji confetti
                    confetti.textContent = emojis[Math.floor(Math.random() * emojis.length)];
                    confetti.style.fontSize = '20px';
                } else {
                    // Color confetti
                    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                    confetti.style.borderRadius = '50%';
                }
                
                const duration = 3000 + Math.random() * 2000;
                confetti.animate([
                    { top: '-20px', opacity: 1 },
                    { top: '100vh', opacity: 0 }
                ], { duration: duration, easing: 'cubic-bezier(0.1,0.8,0.3,1)' });
                
                container.appendChild(confetti);
                setTimeout(() => confetti.remove(), duration);
            }, i * 30);
        }
        
        setTimeout(() => container.remove(), 5000);
    })();
    </script>
    """
    html(confetti_js, height=0, width=0)

def show_balloons():
    # Use Streamlit's built-in balloons which work everywhere
    st.balloons()

def show_snow():
    # Use Streamlit's built-in snow which work everywhere
    st.snow()

# ----------------- Content Collections -----------------
JOKES = [
    "Why don't skeletons fight each other? They don't have the guts!",
    "What do you call a fake noodle? An impasta!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "How do you organize a space party? You planet!",
    "Why did the math book look sad? Because it had too many problems.",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why can't you trust an atom? Because they make up everything!",
    "What did one wall say to the other wall? I'll meet you at the corner!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    "What's orange and sounds like a parrot? A carrot!"
]

GAMES = {
    "Would You Rather": [
        "Have hands for feet or feet for hands?",
        "Live without internet or without air conditioning?",
        "Be able to fly or be invisible?",
        "Have unlimited money or unlimited time?",
        "Live in a castle or on a tropical island?"
    ],
    "Truth or Dare": [
        "Tell me about your happiest memory",
        "Dance to a song for 10 seconds!",
        "What's your most embarrassing moment?",
        "Sing the chorus of your favorite song",
        "What's something you've never told anyone?"
    ],
    "This or That": [
        "Pizza or burgers?",
        "Summer or winter?",
        "Movies or TV shows?",
        "Books or video games?",
        "City life or country life?"
    ]
}

ADVICE = [
    "Try the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste",
    "Write down 3 things you're grateful for today",
    "Take 3 deep breaths - inhale for 4 counts, hold for 7, exhale for 8",
    "When feeling overwhelmed, break tasks into smaller 'bite-sized' pieces",
    "Practice positive self-talk - say kind things to yourself in the mirror",
    "Set small achievable goals to build confidence and momentum",
    "Take regular screen breaks - try the 20-20-20 rule (every 20 minutes, look at something 20 feet away for 20 seconds)",
    "Keep a worry journal - write down concerns and possible solutions",
    "Practice mindfulness by focusing on your current activity without judgment",
    "Connect with nature - even a short walk outside can improve mood"
]

# ----------------- Session State -----------------
if "history" not in st.session_state:
    st.session_state.history = []
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
if "models_loaded" not in st.session_state:
    st.session_state.models_loaded = False
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = None

# ----------------- Helpers -----------------
def add_to_chat(bot_message: str):
    st.session_state.history.append({"user": "", "bot": bot_message})
    st.session_state.show_chat = True
#    show_balloons()  # Show balloons on any interaction

def load_models():
    if not st.session_state.models_loaded:
        with st.spinner("Loading AI models..."):
            st.session_state.emotion_pipe = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base"
            )
            st.session_state.chatbot_pipe = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium"
            )
            st.session_state.models_loaded = True

def detect_emotion(text):
    result = st.session_state.emotion_pipe(text)[0]
    return result['label'], result['score']

def get_bot_reply(user_input):
    response = st.session_state.chatbot_pipe(
        user_input,
        max_length=1000,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
    )
    return response[0]['generated_text']

# ----------------- UI -----------------
st.markdown('<h1 class="title-text">🧠 SentiPal</h1>', unsafe_allow_html=True)
st.markdown('<p class="title-text">Your emotional AI companion 🤖💬</p>', unsafe_allow_html=True)

# Front-page quick-help buttons
st.markdown("### Need some help?")
col1, col2, col3 = st.columns(3)

if col1.button("😂 Tell me a joke", key="main_joke"):
    add_to_chat(random.choice(JOKES))

if col2.button("🎮 Play a game", key="main_game"):
    game_type = random.choice(list(GAMES.keys()))
    question = random.choice(GAMES[game_type])
    add_to_chat(f"Let's play **{game_type}**! {question}")

if col3.button("💡 Get advice", key="main_advice"):
    add_to_chat(f"Here's something to try: {random.choice(ADVICE)}")

# Enhanced Celebration buttons
st.markdown("### Need some cheer?")
celeb_col1, celeb_col2, celeb_col3 = st.columns(3)

if celeb_col1.button("🎉 Confetti", key="confetti"):
    show_confetti()
    add_to_chat("Enjoy the confetti! ✨")

if celeb_col2.button("🎈 Balloons", key="balloons"):
    show_balloons()
    add_to_chat("Here come the balloons! 🎈")

if celeb_col3.button("❄️ Snow", key="snow"):
    show_snow()
    add_to_chat("Snow is falling! ❄️")

# Chat input
user_input = st.text_input("💬 Say something to SentiPal...", key="chat_input")

if st.button("Send", key="send_button") and user_input.strip():
    load_models()
    with st.spinner("SentiPal is thinking..."):
        emotion, confidence = detect_emotion(user_input)
        reply = get_bot_reply(user_input)

        st.session_state.history.append({
            "user": user_input,
            "bot": reply + f"\n\n_(detected emotion: **{emotion}**, {confidence*100:.1f}%)_"
        })
        st.session_state.show_chat = True
        show_balloons()  # Show balloons on message send

# ----------------- Chat Display -----------------
if st.session_state.history:
    chat_visibility = "chat-visible" if st.session_state.show_chat else ""
    st.markdown(f"""
    <div class="chat-container {chat_visibility}">
        <h4>Chat with SentiPal</h4>
    """, unsafe_allow_html=True)

    for item in st.session_state.history:
        if item.get("user"):
            st.markdown(f'<div class="user-message">You: {item["user"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-message">SentiPal: {item["bot"]}</div>', unsafe_allow_html=True)

    if st.button("Close Chat", key="close_chat", type="primary"):
        #st.session_state.show_chat = False
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
        
    st.markdown("</div>", unsafe_allow_html=True)
