import os
import base64
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def process_issue_query(message, image_data=None, conversation_history=None):
    """
    Process a property issue query with an image and conversation context.
    
    Args:
        message (str): User's text message
        image_data (str, optional): Base64 encoded image data
        conversation_history (list, optional): Previous messages in the conversation
        
    Returns:
        str: Agent's response with issue detection and recommendations
    """
    if conversation_history is None:
        conversation_history = []
    
    # Create system prompt
    system_prompt = """
    You are a property issue detection expert. Analyze images of properties to identify visible problems 
    such as water damage, mold, cracks, structural issues, electrical problems, plumbing issues, 
    or other maintenance concerns. dont give me markdown like ** etc just give plain text answers

    When analyzing an image:
    1. Describe what you see in 1-2 sentences
    2. Explain the likely cause
    3. Recommend solutions or next steps (like contacting specific professionals)
    4. Mention any safety concerns if applicable

    For follow-up questions about the image, refer to your previous observations and provide
    more detailed information as requested.
    """
    
    # Convert conversation history to format expected by OpenAI API
    formatted_messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history
    for msg in conversation_history:
        if msg.get('sender') == 'user':
            content = []
            if msg.get('message'):
                content.append({"type": "text", "text": msg.get('message')})
            
            if msg.get('image'):
                img_data = msg.get('image')
                if "base64," in img_data:
                    img_data = img_data.split("base64,")[1]
                
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_data}"
                    }
                })
            
            if content:
                formatted_messages.append({"role": "user", "content": content})
        
        elif msg.get('sender') == 'bot':
            if msg.get('message'):
                formatted_messages.append({"role": "assistant", "content": msg.get('message')})
    
    # Add current message
    current_content = []
    if message:
        current_content.append({"type": "text", "text": message})
    
    if image_data and "base64," in image_data:
        img_data = image_data.split("base64,")[1]
        current_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{img_data}"
            }
        })
    
    if current_content:
        formatted_messages.append({"role": "user", "content": current_content})
    
    try:
        # Call the OpenAI API with the complete conversation
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=formatted_messages,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error processing image or conversation: {str(e)}")
        return "I'm sorry, I couldn't process your request properly. Please try again or describe the issue in more detail."
