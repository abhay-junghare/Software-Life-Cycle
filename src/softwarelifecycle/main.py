import streamlit as st
import json

from src.softwarelifecycle.LLMs.groq_llm import GroqLLM
from src.softwarelifecycle.graph.graph_builder import GraphBuilder
from src.softwarelifecycle.ui.streamlit_ui.display_result import DisplayResultStreamlit
from src.softwarelifecycle.ui.streamlit_ui.load_ui import LoadStreamlitUI



# MAIN Function START
def load_software_life_cycle_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.
    """
    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    # Text input for user message
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe 
    else :
        user_message = st.chat_input("Enter your message:")

    #user_message = "Build a food delivery website"

    if user_message:
        try:
            # Configure LLM
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()
            usecase = "SDLC"

            ### Graph Builder
            graph_builder=GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph("Generate User Stories")
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph setup failed - {e}")
                return

        except Exception as e:
                raise ValueError(f"Error Occurred with Exception : {e}")
        