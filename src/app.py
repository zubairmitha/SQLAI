from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import streamlit as st
from decouple import config

def chat_page():
     #st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_balloon:")

    st.title("Chat with MySQL") #)

    with st.sidebar:
        st.subheader("Settings")
        st.write("This is a simple chat application using MySQL. Connect to the database and start chatting.")
        
        st.text_input("Host", value="localhost", key="Host")
        st.text_input("Port", value="3306", key="Port")
        st.text_input("User", value="admin", key="User")
        st.text_input("Password", type="password", value="Pattern987$", key="Password")
        st.text_input("Database", value="ecommerce_database", key="Database")
        
        if st.button("Connect"):
            with st.spinner("Connecting to database..."):
                db = init_database(
                    st.session_state["User"],
                    st.session_state["Password"],
                    st.session_state["Host"],
                    st.session_state["Port"],
                    st.session_state["Database"]
                )
                st.session_state.db = db
                st.success("Connected to database!")
        
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)

    user_query = st.chat_input("Type a message...")
    if user_query is not None and user_query.strip() != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        
        with st.chat_message("Human"):
            st.markdown(user_query)
            
        with st.chat_message("AI"):
            response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
            st.markdown(response)
            
        st.session_state.chat_history.append(AIMessage(content=response))


def login_page():
    st.markdown('## Chat with SQL AI ⚔️')
    col1, col2 = st.columns((2,1))
    with col1:
        st.markdown(
            f"""
            Chat with SQL AI to ask questions about your database. You can ask questions like:
            - How many customers are there?
            - What is 10 most popluar products?
            - Are sales up this week?


            #### [Sign Up Now 🤘🏻]({config('STRIPE_CHECKOUT_LINK')})
            """
        )
    #with col2:
        #image = Image.open('./assets/DALL·E 2023-01-08 17.53.04 - futuristic knight robot on a horse in cyberpunk theme.png')
        #st.image(image)


    st.markdown('### Already have an Account? Login Below👇🏻')
    with st.form("login_form"):
        st.write("Login")
        email = st.text_input('Enter Your Email')
        password = st.text_input('Enter Your Password')
        submitted = st.form_submit_button("Login")


    if submitted:
        if password == config('SECRET_PASSWORD'):
            st.session_state['logged_in'] = True
            st.text('Succesfully Logged In now!')
            st.switch_page('pages/chat.py')
        else:
            st.text('Incorrect, login credentials.')
            st.session_state['logged_in'] = False

load_dotenv()
st.set_page_config(page_icon='🗡', page_title='Chat with SQL AI')
if 'logged_in' in st.session_state.keys():
    #chat_page()
    st.text('Succesfully Logged In agaiiiiiiiin!')
    st.switch_page('pages/chat.py')
else:
    login_page()
    st.text('not logg!')
    