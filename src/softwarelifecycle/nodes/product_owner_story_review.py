from typing_extensions import Literal
from src.softwarelifecycle.state.state import State
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field


class ProductOwnerStoryReviewNode:
    """
    Review User Stories by product owner
    """
    def __init__(self, model):
        self.llm = model

    def process(self, state:State) -> dict:

        sys_msg = SystemMessage(content = """
        *"You are an experienced Product Owner and Business Analyst collaborating to review requirements and user stories. Your goal is to ensure clarity, completeness, and alignment with business objectives. Please evaluate the following user stories and provide a detailed review using the structured format below:"*

        1. **User Story Review**:
        - **Title**: [User Story Title]
        - **Review Feedback**:
            - Does the story clearly define the user role, action, and outcome?
            - Are the acceptance criteria specific, testable, and measurable?
            - Are there any ambiguities or missing details?
            - Does the story align with the overall product vision and objectives?

        2. **Requirement Analysis**:
        - Are the requirements well-documented and prioritized?
        - Do they consider all relevant stakeholders and scenarios?
        - Are there potential risks or constraints to address?
        - Are there gaps or dependencies that need clarification?

        3. **Suggestions for Improvement**:
        - Provide actionable recommendations to enhance the user stories and requirements.
        - Suggest additional edge cases or scenarios if needed.
        - Highlight any potential areas of refinement for better implementation.

        4. **Validation Checklist**:
        - Ensure each story is INVEST-compliant (Independent, Negotiable, Valuable, Estimable, Small, Testable).
        - Confirm the requirements meet the Definition of Ready (DoR) for development.

        *Example Output*: Summarize the review feedback in a structured, professional format that ensures the user stories and requirements are ready for development.
                
        """)
        
        
        # Augment the LLM with schema for structured output
        evaluator = self.llm.with_structured_output(ProductOwnerReviewFeedback)

        if state.get("product_owner_feedback"):
            print("Product owner review with feedback---------------")
            message = f"""
                Review the below user stories.
                {state['user_story']}
                And Check whether the below feedback is integrated or not while maintaining clarity, completeness, and alignment with business objectives:
                {state['product_owner_feedback']}
                """
            #res = evaluator.invoke([f"Review user stories {state['user_story']}, but check whether the below feedback is integrated or not: {state['product_owner_feedback']}"])
            res = evaluator.invoke([message])
        else:
            print("Product owner review---------------")
            res = evaluator.invoke([sys_msg] + [f" Review user stories {state['user_story']}"])
        print(str(res.grade))
        return {"product_owner_review_status": res.grade, "product_owner_feedback": res.feedback}
    


# Schema for structured output to use in evaluation
class ProductOwnerReviewFeedback(BaseModel):
    
    grade: Literal["Approved", "Not Approved"] = Field(
        description="Decide if the product owner review is approved or not. Also if there is any feedback then make this as Not Approved.",
    )
    feedback: str = Field(
        description="If the product owner review is not approved then provide feedback on how to improve it.",
    )