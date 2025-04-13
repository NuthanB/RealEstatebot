from agents.issue_agent import process_issue_query
from agents.tenancy_agent import process_tenancy_query
import re

# Keywords that might indicate tenancy-related queries
TENANCY_KEYWORDS = [
    'landlord', 'tenant', 'lease', 'rent', 'deposit', 'evict', 'notice', 'agreement',
    'contract', 'tenancy', 'property manager', 'vacate', 'repairs', 'maintenance',
    'rights', 'obligations', 'terminate', 'legal', 'law', 'housing'
]

def route_query(message, image_data=None, conversation_history=None):
    """
    Routes the query to the appropriate agent based on content and conversation history.
    
    Args:
        message (str): The user's text message
        image_data (str, optional): Base64 encoded image data
        conversation_history (list, optional): Previous messages in the conversation
        
    Returns:
        tuple: (agent_type, response)
    """
    if conversation_history is None:
        conversation_history = []
    
    # Check if there's an image in the current message
    has_current_image = bool(image_data)
    
    # Check if there was an image in previous messages
    has_previous_image = any(msg.get('image') for msg in conversation_history if msg.get('sender') == 'user')
    
    # If current message has an image, route to issue detection agent
    if has_current_image:
        return 'issue_agent', process_issue_query(message, image_data, conversation_history)
    
    # If previous messages had images and this is a follow-up, route to issue detection agent
    if has_previous_image:
        # Find the most recent image
        recent_image = None
        for msg in reversed(conversation_history):
            if msg.get('sender') == 'user' and msg.get('image'):
                recent_image = msg.get('image')
                break
        
        if recent_image:
            return 'issue_agent', process_issue_query(message, recent_image, conversation_history)
    
    # Check if the message contains tenancy-related keywords
    message_lower = message.lower()
    
    # Count tenancy-related keywords in the message
    keyword_count = sum(1 for keyword in TENANCY_KEYWORDS if keyword in message_lower)
    
    # If tenancy keywords are found, route to tenancy agent
    if keyword_count > 0:
        return 'tenancy_agent', process_tenancy_query(message, conversation_history)
    
    # If unsure, ask clarifying question
    if not message.strip():
        return 'router', "Please provide more details about your question. Are you asking about a property issue or a tenancy question?"
    
    # Look at conversation history to determine which agent was used previously
    if conversation_history:
        previous_agent = None
        for msg in reversed(conversation_history):
            if msg.get('sender') == 'bot' and msg.get('agent'):
                previous_agent = msg.get('agent')
                break
        
        # Continue with the same agent if there was a previous interaction
        if previous_agent == 'issue_agent':
            return 'issue_agent', process_issue_query(message, None, conversation_history)
        elif previous_agent == 'tenancy_agent':
            return 'tenancy_agent', process_tenancy_query(message, conversation_history)
    
    # Default to tenancy agent for general text queries without context
    return 'tenancy_agent', process_tenancy_query(message, conversation_history)