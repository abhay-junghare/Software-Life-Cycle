import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message
        if usecase =="Basic Chatbot":
            for event in graph.stream({'messages':("user",user_message)}):
                print(event.values())
                for value in event.values():
                    print(value['messages'])
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)

        if usecase == "SDLC":
            # Invoke
            # state = graph.invoke({"topic": ("user",user_message)})
            # print(state)
            
            for event in graph.stream({'topic':("user",user_message)}, stream_mode="values"):
                #print(str(event))
                #print("step 1")    
                if 'user_story' not in event:
                    with st.chat_message("user"):
                        st.write(user_message)
                with st.chat_message("assistant"):
                    if 'user_story' in event and event['user_story'] != '':
                        st.write("User Stories")
                        st.write(event["user_story"])
                    if 'product_owner_review_status' in event and event['product_owner_review_status'] != '':
                        st.write("Review Status")
                        st.write(event["product_owner_review_status"])
                    if 'product_owner_feedback' in event and event['product_owner_feedback'] != '':
                        st.write("Review Feedback")
                        st.write(event["product_owner_feedback"])
                # print("Step 1-Start************************************")
                # print(str(event))
                # print("Step 1-End************************************")
                # for value in event.values():
                #     print("Step 2-##############################################")
                #     print(str(value))
                    # with st.chat_message("user"):
                    #     print("Step 3")
                    #     st.write(user_message)
                    # with st.chat_message("assistant"):
                    #     print("Step 4")
                    #     st.write(value["user_story"])

        elif usecase=="Chatbot with Tool":
             # Prepare state and invoke the graph
            initial_state = {"messages": [user_message]}
            res = graph.invoke(initial_state)
            for message in res['messages']:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message)==ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool Call Start")
                        st.write(message.content)
                        st.write("Tool Call End")
                elif type(message)==AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)
             