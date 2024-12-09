import streamlit as st
import pandas as pd
import io
import base64
from agent import agent ,get_agent_2
from examples import save_liked_answer_to_examples
from langchain_utils import execute_query
from prompts import answer_prompt  
from agent import llm  
from langchain_core.output_parsers import StrOutputParser
from prompts import get_system_suffix_2, set_customer_id
from chat_history import insert_data
from langchain_utils import authenticate, is_authenticated
from feedback import update_feedback_status

# Display heading on both login and chatbox pages
st.markdown(
    "<h1 style='text-align: center; margin-top: -24px;'>Scogo Analytics Chatbot</h1>",
    unsafe_allow_html=True,
)

# Display login form if user is not authenticated
if not is_authenticated():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        token = authenticate(email, password)

        if token:
            st.session_state.token = token
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Login failed. Please check your credentials.")

# Display the main app if user is authenticated
if is_authenticated():
    # Top-right buttons (Refresh and Logout)
    col1, col2, col3 = st.columns([7, 1.5, 1.5])
    with col2:
        if st.button("Refresh", help="Refresh Chat"):
            st.session_state.messages.clear()
            st.session_state.csv = ""
            st.rerun()
    with col3:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "query" not in st.session_state:
        st.session_state.query = None
    if "csv" not in st.session_state:
        st.session_state.csv = None
    if "customer_id" not in st.session_state:
         st.session_state.customer_id = []   
    if "fk_user_id" not in st.session_state:
        st.session_state.fk_user_id=[]                   

    # Chat input at the bottom of the page 
    prompt = st.chat_input("Ask your NL2SQL Question...")

    # Process input only if a prompt is provided
    if prompt:
        st.session_state.prompt = prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # chat_history = create_history(st.session_state.messages)
        customer_id = st.session_state.get('customer_id', None)
        fk_user_id = st.session_state.get('fk_user_id',None)

        system_suffix_2 = get_system_suffix_2(customer_id)
        
        history_string = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages if msg['role'] == "user"])
        print("history_string:", history_string)

        with st.spinner("Generating response..."):
            query_list = []
            try:
                if st.session_state['customer_id']: 
                    few_shot_prompt_2 = set_customer_id(customer_id)
                    agent_2 = get_agent_2(few_shot_prompt_2)
                    response = agent_2.invoke({"input": f"{history_string}\nuser: {prompt}"})
                    # response = agent_2.invoke({"input": f"{history_string}\nuser: {prompt}"})
                    # print("Agent Response: ", response)

                    # print("few_shot_prompt:", few_shot_prompt)
                    for toolcall in response['intermediate_steps']:
                        if (toolcall[0].tool == 'sql_db_query' and toolcall[0].tool_input is not None):
                            query = toolcall[0].tool_input['query']
                            print("query:", query)
                            query_list.append(query)
                                    
                    insert_data = insert_data(fk_user_id,prompt,query_list[-1])
                    df = execute_query(query_list[-1])
                    st.session_state.query = query_list[-1] 
                    print(f"Query : {query_list}")

                    if df.empty:
                        # st.warning("No results found for the query.")
                        st.session_state.messages.append({"role": "assistant", "content": "No Data Found."})

                    else:
                    # Check the number of rows in the DataFrame
                        if len(df) == 1:
                            # Rephrase the result if only one row is present
                            result_text = df.to_string(index=False)  # Convert the row to a string
                            print("result_text:",result_text)
                            rephrase_answer = answer_prompt | llm | StrOutputParser()  
                            rephrased_result = rephrase_answer.invoke({"question": prompt, "query": query_list[-1], "result": result_text})
                            st.session_state.messages.append({"role": "assistant", "content": rephrased_result})
                        else:
                            # Display the DataFrame if more than one row is present
                            st.session_state.messages.append({"role": "result", "content": df.to_csv(index=False)})

                else :
                    response = agent.invoke({"input": f"{history_string}\nuser: {prompt}"})
                    # print("Agent Response: ", response)

                    # print("few_shot_prompt:", few_shot_prompt)
                    for toolcall in response['intermediate_steps']:
                        if (toolcall[0].tool == 'sql_db_query' and toolcall[0].tool_input is not None):
                            query = toolcall[0].tool_input['query']
                            # print("query:", query)
                            query_list.append(query)
                            # st.session_state.query = query_list[-1]  # Store the query in the session state
                            # print(f"Query : {query_list}")

                    print(f"Query : {query_list}") 
                    insert_data = insert_data(fk_user_id,prompt,query_list[-1])
                    df = execute_query(query_list[-1])
                    st.session_state.query = query_list[-1] 

                    # print("DF:", df)

                    if df.empty:
                        # st.warning("No results found for the query.")
                        st.session_state.messages.append({"role": "assistant", "content": "No Data Found."})
                    
                    else:
                    # Check the number of rows in the DataFrame
                        if len(df) == 1:
                            # Rephrase the result if only one row is present
                            result_text = df.to_string(index=False)  # Convert the row to a string
                            rephrase_answer = answer_prompt | llm | StrOutputParser()  
                            rephrased_result = rephrase_answer.invoke({"question": prompt, "query": query_list[-1], "result": result_text})
                            st.session_state.messages.append({"role": "assistant", "content": rephrased_result})
                        else:
                            # Display the DataFrame if more than one row is present
                            st.session_state.messages.append({"role": "result", "content": df.to_csv(index=False)})

            except Exception as e:
                    st.session_state.messages.append({"role": "assistant", "content": "No Data Found."})
                    print(f"Error occurred: {e}")
    
    # Display previous messages and results
    for index, message in enumerate(st.session_state.messages):
        # print(st.session_state)
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        elif message["role"] == "assistant":
            st.chat_message("assistant").markdown(message["content"])

            # Display like/dislike buttons below the rephrased response
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("👍", key=f"like_assistant_{index}"):
                    if "query" in st.session_state and "prompt" in st.session_state:
                        save_liked_answer_to_examples(st.session_state.prompt, st.session_state.query)
                        update_feedback_status(st.session_state.fk_user_id, 'like', st.session_state.prompt, st.session_state.query)

                        st.success("Liked! The answer has been saved for future use.")
            with col2:
                if st.button("👎", key=f"dislike_assistant_{index}"):
                    st.warning("Thank You. Your feedback will help improve the system.")
                    update_feedback_status(st.session_state.fk_user_id, 'dislike', st.session_state.prompt, st.session_state.query)

        
        elif message["role"] == "result":
            # Convert CSV string back to DataFrame
            if message["content"]:
                df = pd.read_csv(io.StringIO(message["content"]))
                st.dataframe(df)

                # Generate CSV download link
                b64 = base64.b64encode(message["content"].encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="query_result.csv">Download CSV File</a>'
                st.markdown(href, unsafe_allow_html=True)

                # Display like/dislike buttons below the DataFrame result
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("👍", key=f"like_result_{index}"):
                        if "query" in st.session_state and "prompt" in st.session_state:
                            save_liked_answer_to_examples(st.session_state.prompt, st.session_state["query"])
                            update_feedback_status(st.session_state.fk_user_id, 'like', st.session_state.prompt, st.session_state.query)

                            st.success("Liked! The result has been saved for future use.")
                with col2:
                    if st.button("👎", key=f"dislike_result_{index}"):
                        st.warning("Thank You. Your feedback will help improve the system.")
                        update_feedback_status(st.session_state.fk_user_id, 'dislike', st.session_state.prompt, st.session_state.query)

else:
    st.warning("Please login to access the chatbot.")


