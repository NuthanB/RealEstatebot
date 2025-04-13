import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def process_tenancy_query(message, conversation_history=None):
    """
    Process a tenancy-related query with conversation context.
    
    Args:
        message (str): User's question about tenancy
        conversation_history (list, optional): Previous messages in the conversation
        
    Returns:
        str: Agent's response with tenancy information
    """
    if conversation_history is None:
        conversation_history = []
    
    # Create a system prompt
    system_prompt = """
    You are a tenancy law specialist who provides accurate information about rental agreements, 
    tenant-landlord relationships, and housing regulations and never say that i am unable to provide legal advice , be very kind and answer the question Your responses should be: 
    
    1. Factual and based on common tenancy laws
    2. Clear about when laws might vary by location
    3. Helpful in explaining tenant and landlord rights and responsibilities
    4. Educational about proper procedures in tenancy situations
    5. Always ask which place the user is in to provide the most relevant information
    
    If the user mentions a specific location, tailor your response to that jurisdiction if you have 
    knowledge about it. Otherwise, provide general guidance while noting that laws vary by location.
    
    Always suggest consulting local housing authorities or a legal professional for specific legal advice.
    """
    
    # Convert conversation history to format expected by OpenAI API
    formatted_messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history
    for msg in conversation_history:
        if msg.get('sender') == 'user' and msg.get('message'):
            formatted_messages.append({"role": "user", "content": msg.get('message')})
        elif msg.get('sender') == 'bot' and msg.get('message'):
            formatted_messages.append({"role": "assistant", "content": msg.get('message')})
    
    # Add current message
    if message:
        formatted_messages.append({"role": "user", "content": message})
    
    try:
        # Call the OpenAI API with the complete conversation
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=formatted_messages,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error processing conversation: {str(e)}")
        return "I'm sorry, I'm having trouble answering your tenancy question right now. Please try again or rephrase your question."
