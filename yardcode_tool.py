import requests
import os

# The FREE YardCode Validation Endpoint URL (No API Key needed for this endpoint)
# I useD this to prove successful API communication with the YardCode platform
VALIDATE_URL = "https://www.yardcode.ng/api/validate?yard_code={yard_code}"

def validate_yardcode_tool(yard_code: str) -> str:
    """
    TOOL: Calls the FREE YardCode API endpoint to validate a YardCode's format.
    This demonstrates the agent's ability to integrate with an external API.
    """
    if not yard_code:
        return "ERROR: YardCode cannot be empty."

    try:
        # I used a live HTTP request to the actual YardCode API (FREE endpoint)
        # Note: I removed spaces because the API expects the code to be contiguous
        url = VALIDATE_URL.format(yard_code=yard_code.replace(" ", ""))
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Raise exception for bad status codes

        data = response.json()
        
        # Checking the actual JSON response from the YardCode server
        if data.get("status") == "success":
            return f"Validation SUCCESS: YardCode '{yard_code}' is correctly formatted and confirmed by YardCode API. Dispatch Ready."
        else:
            return f"Validation FAILED: API could not confirm the YardCode format."

    except requests.exceptions.RequestException as e:
        return f"YardCode API Connection Error: Could not reach server. Details: {e}"

# --- Simple execution check ---
if __name__ == "__main__":
    print("--- Running YardCode Tool PoC Check (Live Call) ---")
    
    # Using a known good YardCode from the documentation
    sample_yardcode = "GQ9U88levi" 
    result = validate_yardcode_tool(sample_yardcode)
    
    print(f"YardCode Input: {sample_yardcode}")
    print(f"Tool Result: {result}")