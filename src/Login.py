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

def login_page():
    st.markdown('## Chat with SQL AI')
    col1, col2 = st.columns((2,1))
    with col1:
        st.markdown(
            f"""
            Chat with SQL AI to ask questions about your database. You can ask questions like:
            - How many products do we have?
            - What are the 10 most popluar products?
            - Are orders up this week?


            **[Sign Up Now]({config('STRIPE_CHECKOUT_LINK')})**
            """
        )



    st.markdown('### Already have an Account? Login Below')
    with st.form("login_form"):
        st.write("Login")
        email = st.text_input('Enter Your Email')
        password = st.text_input('Enter Your Password')
        submitted = st.form_submit_button("Login")


    if submitted:
        if password == config('SECRET_PASSWORD'):
            st.session_state['logged_in'] = True
            st.text('Succesfully Logged In!')
            st.switch_page('pages/chat.py')
        else:
            st.text('Incorrect, login credentials.')
            st.session_state['logged_in'] = False


load_dotenv()
st.set_page_config(page_icon='🗡', page_title='Chat with SQL AI')
if 'logged_in' in st.session_state.keys():
    st.switch_page('pages/chat.py')
else:
    login_page()
    