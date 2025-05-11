
import re
from typing import List, Dict, Tuple
from google.adk.agents import Agent
from pydantic import BaseModel, Field

import pandas as pd


# Load Excel file
HSN_EXCEL_PATH = "HSN_SAC.xlsx"

hsn_df = pd.read_excel(HSN_EXCEL_PATH, dtype={'A': str})

hsn_df['A'] = hsn_df['A'].astype(str)
hsn_dict = dict(zip(hsn_df['A'], hsn_df['Description']))

min_len = hsn_df['A'].str.len().min()
max_len = hsn_df['A'].str.len().max()

def extract_codes(prompt: str) -> List[str]:
    return re.findall(r'\b\d+\b', prompt)

def validate_code_length(code: str) -> bool:
    return min_len <= len(code) <= max_len

def lookup_description(code: str) -> Tuple[str, str]:
    if code in hsn_dict:
        if len(code) == 2:
            return (code, f"Chapter {code}: {hsn_dict[code]}")
        return (code, hsn_dict[code])
    else:
        return (code, "Data not found for this HSN code.")

def process_prompt(prompt: str) -> Dict[str, str]:
    codes = extract_codes(prompt)
    if not codes:
        return {"error": "No HSN codes found in your input. Please enter at least one valid HSN code."}
    results = {}
    for code in codes:
        if not validate_code_length(code):
            results[code] = f"Invalid HSN code: '{code}' is not of valid length ({min_len}-{max_len} digits)."
        else:
            code_result, desc = lookup_description(code)
            results[code] = desc
    return results

class DescriptionOutput(BaseModel):
    code: str = Field(description="HSN code")
    description: str = Field(description="Description/chapter name or error message for the code")

class HSNAgent(Agent):
    def __init__(self):
        super().__init__(
            name="test_agent",
            model="gemini-1.5-flash",
            description="Agent for validating and describing HSN codes.",
            instruction=(
                "You are an agent that validates HSN codes from user input, "
                "checks their length, looks up their descriptions, and provides detailed feedback."
                " If the code is invalid or not found, return an appropriate error message."
                " The HSN codes are 2 to 8 digits long. "
                "if the code is 2 digits long, return the chapter "
            ),
        )

    def handle(self, prompt: str) -> List[DescriptionOutput]:
        results = process_prompt(prompt)
        if "error" in results:
            return [DescriptionOutput(code="", description=results["error"])]
        return [DescriptionOutput(code=code, description=desc) for code, desc in results.items()]
    
root_agent = HSNAgent()


