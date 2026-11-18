
import streamlit as st

st.set_page_config(
    page_title="BJAK Personal AI Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("Personal AI Interview Assistant")
st.caption("BJAK Engineering Manager / Lead Engineer Assessment")

st.write(
    "Ask questions about my professional background, "
    "technical experience, and engineering projects."
)

question = st.text_input(
    "Your question",
    placeholder="What is your experience with Python?"
)

if st.button("Ask Assistant"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        st.info(
            "The knowledge retrieval engine is not connected yet. "
            "We'll implement grounded answers in the next step."
        )

st.divider()
st.caption("Answers will be supported by verified knowledge sources.")
