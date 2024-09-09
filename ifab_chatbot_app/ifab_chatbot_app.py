import uuid
import streamlit as st
import rag
import os
import database as db

def get_response(message):
    question = message
    context = rag.retrieve_context(question, 5)
    prompt = rag.create_prompt(question, context)
    answer = rag.query_llm(prompt)
    return f"Bot: {answer}"

def main():
    st.title("Ask IFAB")
    
    # Define custom styles for text boxes - applying to both text input and text area
    custom_css = """
    <style>
        textarea, .stTextInput > div > div > input {
            border: 2px solid black !important;
        }
    </style>
    """
    # Inject styles to html
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Input for user message
    user_message = st.text_input("You: ", key="user_message")

    # Ensure unique keys for buttons so that they do not conflict and are distinguishable
    send_button_pressed = st.button("Send", key="send_button")


    feedback_state = db.get_state()
    st.session_state["likes"] = feedback_state['cnt_positive']
    st.session_state["dislikes"] = feedback_state['cnt_negative']

    if send_button_pressed:
        if user_message:
            # Get response from the bot and save it to session state
            bot_response = get_response(user_message)
            st.session_state["response"] = bot_response
            st.session_state["qna_id"] = str(uuid.uuid1())            
            db.insert_record_qna(st.session_state["qna_id"] ,user_message,bot_response)
        else:
            st.warning("Please type a query.")

    # Verify response existence in session state and display it
    if "response" in st.session_state:
        bot_response = st.session_state["response"]
        st.text_area("Chat", value=bot_response, height=200, max_chars=None, key="response_area")
        
        col1, col2 = st.columns(2)
        with col1:
            # Like button with unique key management
            if st.button("👍", key="like_button"):
                db.insert_record_feedback( st.session_state["qna_id"], True)
                st.session_state["likes"] = st.session_state.get("likes", 0) + 1
        with col2:
            # Dislike button with unique key management
            if st.button("👎", key="dislike_button"):
                db.insert_record_feedback( st.session_state["qna_id"], False)
                st.session_state["dislikes"] = st.session_state.get("dislikes", 0) + 1

        # Display like and dislike counts
        st.write("Likes:", st.session_state.get("likes", 0))
        st.write("Dislikes:", st.session_state.get("dislikes", 0))

if __name__ == '__main__':
    main()