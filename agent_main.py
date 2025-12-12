import os
from dotenv import load_dotenv 
from openai import OpenAI 
from yardcode_tool import validate_yardcode_tool

# --- Secure API Key Loading ---
# This line loads the OPENROUTER_API_KEY from the local, untracked .env file.
# The .env file is excluded from GitHub via the .gitignore file.
load_dotenv() 
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") 
# -----------------------------------------------------------

# --- Initialize OpenRouter Client ---
client = OpenAI(
    api_key=OPENROUTER_API_KEY, 
    base_url="https://openrouter.ai/api/v1" 
)

# --- Tool and Prompt Setup (The Agentic System) ---
# I used a confirmed free Llama model (Meta AI Resource)
LLAMA_MODEL = "meta-llama/llama-3-8b-instruct"
ORDER_DATABASE = {
    # This simulates the MSME's data
    "001": {"status": "Ready for Fitting", "customer": "Aisha"},
    "002": {"status": "Ready for Dispatch", "customer": "Chinedu", "delivery_code": "GQ9U88levi"},
}

def run_llama_agent(user_input: str) -> str:
    """
    This function contains the core Agentic AI logic. It demonstrates the decision 
    to call an external tool (YardCode) versus engaging in conversation (Llama).
    """
    
    print(f"\n[USER QUERY]: {user_input}")

    # 1. Tool Call Logic: My agent checks for keywords related to delivery/verification
    if "dispatch" in user_input.lower() or "verify address" in user_input.lower():
        yardcode_to_check = ORDER_DATABASE.get("002", {}).get("delivery_code", "ERROR")
        
        print(f"\n[AGENT THOUGHT - CRITICAL STEP]: The agent detects the need for external verification. Calling the validate_yardcode_tool('{yardcode_to_check}') to fulfill the request.")
        
        # EXECUTE THE EXTERNAL TOOL
        validation_result = validate_yardcode_tool(yardcode_to_check)
        
        # Llama generates the final response using the tool result
        system_prompt = f"""
        You are 'iPatch', the professional CRM Agent for 'The Stylist' Tailor Shop. The customer is asking for final dispatch of Order 002.
        The result of the address verification tool call was: "{validation_result}".
        Based on this result, you must provide a final, confident response to the customer. Your response will confirm that the dispatch is proceeding using the verified YardCode.
        """
    else:
        # 2. Simple chat logic: If no tool is needed, the agent handles the query conversationally.
        status = ORDER_DATABASE.get("001", {}).get("status", "Not Found")
        system_prompt = f"""
        You are 'iPatch', the CRM Agent for 'The Stylist'. The status of Order 001 is '{status}'.
        Answer the user's query about order status politely and concisely. I designed this logic to handle simple status updates autonomously.
        """

    # 3. Call the Live Llama Model via OpenRouter
    try:
        response = client.chat.completions.create(
    model=LLAMA_MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ],
    stream=False,
    timeout=45 # Added 45 second timeout for free-tier model latency
)
        return response.choices[0].message.content
        
    except Exception as e:
        return f"LLAMA/OPENROUTER ERROR: Failed to get response. Please check your network connection or OpenRouter credit limit. Details: {e}"

# --- Main Program Execution (The Demonstration) ---
if __name__ == "__main__":
    
    # I designed the main execution to showcase both the conversational and tool-calling capabilities.
    
    print("\n" + "="*50)
    print("--- TEST CASE 1: Status Query (Dialogue Only) ---")
    print("= This demonstrates the agent's basic CRM conversation =")
    print("="*50)
    response1 = run_llama_agent("What is the status of my order 001?")
    print(f"\nFinal Agent Response:\n{response1}")

    
    print("\n" + "="*50)
    print("--- TEST CASE 2: Tool Call & Verification ---")
    print("= This demonstrates the required YardCode API integration =")
    print("="*50)
    response2 = run_llama_agent("I need to dispatch my order 002 now. Can you verify the delivery address and confirm?")
    print(f"\nFinal Agent Response:\n{response2}")