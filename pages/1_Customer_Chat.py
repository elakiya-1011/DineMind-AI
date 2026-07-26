import streamlit as st
from components.header import render_hero, load_css
from components.sidebar import render_sidebar
from backend.chains.rag_chain import DineMindOrchestrator
from backend.memory.chat_memory import ChatMemoryManager

st.set_page_config(
    page_title="Customer Assistant - DineMind AI",
    page_icon="💬",
    layout="wide"
)

# Load CSS & Sidebar
load_css()
render_sidebar()

# Initialize Session States
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = DineMindOrchestrator()

if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = ChatMemoryManager()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to DineMind Bistro! 🍽️ I am your AI Customer Assistant. Ask me anything about our menu, dietary options, policies, or say **'Add 1 Margherita Pizza'** to start a simulated order!"}
    ]

# Header Banner
render_hero(
    title="Customer AI Concierge & Order Assistant",
    subtitle="Ask about menus, opening hours, dietary options, or place a simulated food order in natural language.",
    icon="💬"
)

# Top Bar: Cart Status & Clear Chat Controls
cart_count = sum(i["qty"] for i in st.session_state.cart)
cart_total = sum(i["qty"] * i["price"] for i in st.session_state.cart)

col_cart, col_clear = st.columns([4, 1])
with col_cart:
    st.markdown(f"🛒 **Session Cart:** `{cart_count} item(s)` | Subtotal: `${cart_total:.2f}`")

with col_clear:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_memory.clear()
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat transcript reset. How may I assist you?"}
        ]
        st.rerun()

# Expanded Suggested Questions Categorized Accordion / Chips
st.markdown("##### 💡 Suggested Prompts (Click to Ask)")
tab_gen, tab_menu, tab_ord, tab_pol = st.tabs(["👋 Greetings & General", "🍕 Menu & Dietary", "🛒 Simulated Ordering", "📜 Policies & Offers"])

selected_suggestion = None

with tab_gen:
    gen_q = ["Hello! How are you?", "What are your opening hours?", "Where are you located?", "What payment methods do you accept?"]
    c1, c2, c3, c4 = st.columns(4)
    for idx, q in enumerate(gen_q):
        with [c1, c2, c3, c4][idx]:
            if st.button(q, key=f"gen_{idx}", use_container_width=True):
                selected_suggestion = q

with tab_menu:
    menu_q = ["Which dishes are vegetarian?", "Which dishes are vegan?", "Which dishes contain peanuts?", "Recommend something spicy"]
    c1, c2, c3, c4 = st.columns(4)
    for idx, q in enumerate(menu_q):
        with [c1, c2, c3, c4][idx]:
            if st.button(q, key=f"menu_{idx}", use_container_width=True):
                selected_suggestion = q

with tab_ord:
    ord_q = ["Add 1 Margherita Pizza", "Add 2 Cokes", "Show my cart", "Place my order"]
    c1, c2, c3, c4 = st.columns(4)
    for idx, q in enumerate(ord_q):
        with [c1, c2, c3, c4][idx]:
            if st.button(q, key=f"ord_{idx}", use_container_width=True):
                selected_suggestion = q

with tab_pol:
    pol_q = ["Do you provide home delivery?", "Can I reserve a table?", "What is your cancellation policy?", "What discounts are available?"]
    c1, c2, c3, c4 = st.columns(4)
    for idx, q in enumerate(pol_q):
        with [c1, c2, c3, c4][idx]:
            if st.button(q, key=f"pol_{idx}", use_container_width=True):
                selected_suggestion = q

st.markdown("---")

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input Handler
prompt_input = st.chat_input("Type your question or ordering command...")
user_query = selected_suggestion or prompt_input

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Processing request & verifying facts..."):
            answer, trace_dict = st.session_state.orchestrator.process_query(
                user_query,
                st.session_state.chat_memory,
                st.session_state.cart
            )
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    
    if selected_suggestion:
        st.rerun()
