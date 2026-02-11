import os
import json
import requests
import streamlit as st

CHATBOT_URL = os.getenv(
    "CHATBOT_URL", "http://localhost:8000/hospital-rag-agent"
)


st.title("Hosto-bot")
st.info("Feel free to ask me about patients, hospital visits, insurance payers, healthcare providers, reviews, and wait times!")

if "messages" not in st.session_state:
    st.session_state.messages = []

def display_explanation(explanation):
    """Displays agent thought steps in a professional, collapsible container."""
    if not explanation:
        return

    # Use a status container to group 'Behind the scenes' logic
    with st.status("🔍 Viewing execution path...", expanded=False) as status:
        for step in explanation:
            if "🔧 Calling tool" in step:
                st.markdown(f"**Action:** {step}")
            elif "💡 Thought" in step:
                st.caption(step)
            elif "✅ Result" in step:
                st.code(step, language="json")
        status.update(label="✅ Search complete", state="complete")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            display_explanation(message["explanation"])

if prompt := st.chat_input("How can I help you today?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Searching..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            res_json = response.json()
            output_text = res_json["output"]
            explanation = res_json["intermediate_steps"]

        else:
            output_text = "ERROR"
            explanation = []

    st.chat_message("assistant").markdown(output_text)

    display_explanation(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )
