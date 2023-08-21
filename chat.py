import streamlit as st
import random
import time
import timeit
from src.utils import setup_dbqa
from PIL import Image

import streamlit as st
import base64

LOGO_IMAGE = "xft.png"

st.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:50px !important;
        color: #a583e2 !important;
        padding-left: 3%;
    }
    .logo-img {
        float:right;
        object-fit: scale-down;
        padding-bottom: 1%
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p class="logo-text">Document Chatbot</p> </img>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        start = timeit.default_timer()
        dbqa = setup_dbqa()
        full_response = dbqa({'query': prompt})
        end = timeit.default_timer()
        assistant_response = random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help?",
            ]
        )
        # Simulate stream of response with milliseconds delay
        if len(full_response)>0:
            chunk_response=""
            for chunk in full_response["result"].split():
                chunk_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(chunk_response + "▌")
            message_placeholder = st
            #message_placeholder.markdown(full_response["result"])
            # Process source documents
            source_docs = full_response['source_documents']
            message_placeholder.markdown(':timer_clock: :red['+str(round((end - start),2))+'] sec.')
            message_placeholder.markdown(':blue[Reference Document(s)]')
            for i, doc in enumerate(source_docs):
                #message_placeholder.markdown('Source Text: :red['+ str(doc.page_content)+']')
                message_placeholder.markdown('Document Name: :green['+ str(doc.metadata["source"]+']'))
                message_placeholder.markdown('Page Number: :red['+ str(doc.metadata["page"])+']')
                with st.expander("See Document Content"):
                    st.write(str(doc.page_content))
                #message_placeholder.markdown('Document Content: :green['+ str(doc.page_content) +']')
             # Add assistant response to chat history    
            st.session_state.messages.append({"role": "assistant", "content": full_response["result"]})
            # st.session_state.messages.append({"role": "assistant", "content": ':timer_clock: :red['+str(round((end - start),2))+'] sec.'})
            # for i, doc in enumerate(source_docs):
            #     st.session_state.messages.append({"role": "assistant", "content": 'Document Name: :green['+ str(doc.metadata["source"]+']')})
            #     st.session_state.messages.append({"role": "assistant", "content": 'Page Number: :red['+ str(doc.metadata["page"])+']'})
        else:
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
   