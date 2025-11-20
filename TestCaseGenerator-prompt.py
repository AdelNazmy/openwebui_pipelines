"""
title: Example Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for the filter operations."
        )
        max_turns: int = Field(
            default=8, description="Maximum allowable conversation turns for a user."
        )
        pass

    class UserValves(BaseModel):
        max_turns: int = Field(
            default=4, description="Maximum allowable conversation turns for a user."
        )
        pass

    def __init__(self):
        # Indicates custom file handling logic. This flag helps disengage default routines in favor of custom
        # implementations, informing the WebUI to defer file-related operations to designated methods within this class.
        # Alternatively, you can remove the files directly from the body in from the inlet hook
        # self.file_handler = True

        # Initialize 'valves' with specific configurations. Using 'Valves' instance helps encapsulate settings,
        # which ensures settings are managed cohesively and not confused with operational flags like 'file_handler'.
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify the request body or validate it before processing by the chat completion API.
        # This function is the pre-processor for the API where various checks on the input can be performed.
        # It can also modify the request before sending it to the API.
        print(f"inlet:{__name__}")
        print(f"inlet:body:{body}")
        print(f"inlet:user:{__user__}")
        messages = body.get("messages", [])
        try:
            user_message = messages[-1]["content"]
        except:
            user_message = messages[0]["content"]
        if len(user_message) < 5:
            user_message = """### **The Master Prompt for AI Test Case Generation**

**Act as an expert QA (Quality Assurance) Analyst. Your task is to analyze the provided solution design document and generate a comprehensive set of test cases.**

**Objective:** Create a structured test suite that validates the functionality, edge cases, and error conditions of the system described in the requirements.

**Output Format Requirements:**
Present the test cases in a clear, tabular format with the following columns:
*   **Test Case ID:** A unique identifier (e.g., TC-AUTH-01).
*   **Category:** A brief, clear description of what is being tested.
*   **Test Case Description:** A brief, clear description of what is being tested.
*   **Preconditions:** Any necessary system state or user prerequisites before executing the test.
*   **Test Steps:** A detailed, step-by-step sequence of actions to perform.
*   **Test Data:** Specific input values to use (e.g., email: testuser@example.com).
*   **Expected Result:** The precise outcome that verifies the test is successful.

**Specific Instructions for Generation:**

1. **Coverage:** Ensure test cases cover:
    *   **Positive/Happy Path:** Standard, successful workflows.
    *   **Negative Paths:** Invalid inputs, error conditions, and validations (e.g., wrong email format, expired link).
    *   **Edge Cases:** Boundary conditions and unusual but possible scenarios.
    *   **Data Validation:** Rules for input fields (e.g., password complexity).
    *   **Business Logic:** Core rules from the requirements (e.g., link validity period).

2.  **Clarity & Specificity:** Write test steps that are unambiguous and repeatable. Avoid vague terms like "check if it works."

3.  **Prioritization:** If possible, indicate the priority of the test case (e.g., High, Medium, Low) based on its criticality to the core functionality.

**Final Request:**
After generating the table, provide a brief summary stating the total number of test cases and the categories they fall into (e.g., Generated 12 test cases: 4 Positive, 5 Negative, 3 Edge Cases.)
            """
        messages = messages[:-1] + [{"role": "user", "content": user_message}]
        body["messages"] = messages
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify or analyze the response body after processing by the API.
        # This function is the post-processor for the API, which can be used to modify the response
        # or perform additional checks and analytics.
        print(f"outlet:{__name__}")
        print(f"outlet:body:{body}")
        print(f"outlet:user:{__user__}")

        return body