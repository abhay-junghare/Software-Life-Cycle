from src.softwarelifecycle.state.state import State
from langchain_core.messages import SystemMessage


class GenerateUserStoriesNode:
    """
    Generate User Stories implementations
    """
    def __init__(self, model):
        self.llm = model

    def process(self, state:State) -> dict:

        if state.get("product_owner_feedback"):
            message = f"""
                Based on the following feedback:
                {state['product_owner_feedback']}
                Refine and regenerate the below user stories to address the feedback while maintaining clarity, completeness, and alignment with business objectives.
                {state['user_story']}
                """
            msg = self.llm.invoke(message)

            # msg = self.llm.invoke( [sys_msg] + 
            #     [f"Write a user stories about {state['topic']} but take into account the feedback: {state['product_owner_feedback']}"]
            # )
        else:
            sys_msg = SystemMessage(content = """
                You are an experienced Product Owner and Business Analyst skilled in understanding customer needs and translating them into actionable user stories. Please generate detailed all different user stories based on the following context:

                **Title**: [User Story Title]
                Project Overview: [Provide a brief summary of the product or system, including its purpose and target audience.]
                Feature Description: [Outline the feature or functionality that needs user stories.]
                User Roles: [Define the specific user roles, such as end users, administrators, or third-party integrations.]
                Acceptance Criteria: [Specify measurable and testable conditions for completing the user stories.]
                Constraints or Limitations: [Mention any technical, business, or operational constraints that must be considered. Also consider edge cases and potential risks.]
                """)
            msg = self.llm.invoke([sys_msg] + [f"Write a user stories about {state['topic']}"])
    
        return {"user_story": msg.content}