from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage

class State(TypedDict):
    """
    Represents the structure of the state used in the graph.
    """
    #messages: Annotated[list, add_messages]
    topic: str
    user_story: str
    product_owner_review_status: str
    product_owner_feedback: str
    
#class ReviewState(TypedDict):
    

# # Graph state
# class State(TypedDict):
#     joke: str
#     topic: str
#     feedback: str
#     funny_or_not: str