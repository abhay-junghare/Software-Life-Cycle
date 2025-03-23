from langgraph.graph import StateGraph, START,END, MessagesState
from langgraph.prebuilt import tools_condition,ToolNode
from langchain_core.prompts import ChatPromptTemplate
from src.softwarelifecycle.nodes.product_owner_story_review import ProductOwnerStoryReviewNode
from src.softwarelifecycle.state.state import State
from src.softwarelifecycle.nodes.generate_user_stories import GenerateUserStoriesNode

from src.softwarelifecycle.tools.search_tool import get_tools, create_tool_node

class GraphBuilder:

    def __init__(self, model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def generate_user_stories(self):
        """
        Builds a generate user stories graph using LangGraph.
        This method initializes a user stories node using the `GenerateUserStoriesNode` class 
        and integrates it into the graph. The user stories node is set as both the 
        entry and exit point of the graph.
        """
        ## Define the tool and tool node
        # tools=get_tools()
        # tool_node=create_tool_node(tools)

        ##Define LLM
        llm = self.llm

        self.user_stories_node = GenerateUserStoriesNode(self.llm)
        self.product_owner_review_node = ProductOwnerStoryReviewNode(self.llm)

        self.graph_builder.add_node("user_stories", self.user_stories_node.process)
        self.graph_builder.add_node("product_owner_review", self.product_owner_review_node.process)

        self.graph_builder.add_edge(START, "user_stories")
        self.graph_builder.add_edge("user_stories", "product_owner_review")
        
        #self.graph_builder.add_edge("user_stories", END)
        #chatbot_node = obj_chatbot_with_node.create_chatbot(tools)
        
        self.graph_builder.add_conditional_edges("product_owner_review", self.route_review,
                                                 {
                                                     # Name returned by route_review : Name of next node to visit
                                                    "Accepted": END,
                                                    "Rejected + Feedback": "user_stories"
                                                 })


    # Conditional edge function to route back to joke generator or end based upon feedback from the evaluator
    def route_review(self, state: State):
        """Route back to user stories or end based upon feedback from the product owner review"""

        if state["product_owner_review_status"] == "Approved":
            return "Accepted"
        elif state["product_owner_review_status"] == "Not Approved":
            return "Rejected + Feedback"
        




    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Generate User Stories":
            self.generate_user_stories()
        
        
        return self.graph_builder.compile()