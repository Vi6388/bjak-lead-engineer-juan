
import streamlit as st
from answer_engine import answer_question

st.set_page_config(
    page_title="Personal AI Interview Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("Personal AI Interview Assistant")
st.caption("BJAK Engineering Manager / Lead Engineer Assessment")

st.write(
    "Ask questions about my professional background, "
    "engineering projects, and technical experience."
)

examples = [
    "What is your experience with React?",
    "What did you build at Chewy?",
    "Have you built RAG applications?",
    "What is your experience with PostgreSQL?",
    "Did you work at Google?",
]

question = st.selectbox(
    "Example questions",
    ["Enter my own question"] + examples,
)

if question == "Enter my own question":
    question = st.text_input(
        "Your question",
        placeholder="Ask about my professional experience...",
    )

if st.button("Ask Assistant", type="primary"):
    with st.spinner("Searching verified sources..."):
        result = answer_question(question)

    if result["status"] == "answered":
        st.success("Evidence found")
        st.markdown(result["answer"])

        st.subheader("Supporting Sources")

        for source in result["citations"]:
            title = source.get(
                "title",
                source["id"],
            )
            page = source.get("page", "N/A")

            st.caption(
                f"Source: {title} | Page: {page}"
            )

    elif result["status"] == "error":
        st.error(result["answer"])

    else:
        st.warning(result["answer"])
        st.caption(
            "No sufficiently supported answer "
            "was found in the available sources."
        )

st.divider()
st.caption(
    "Answers are derived from documented professional "
    "experience. Unsupported claims are not permitted."
)
