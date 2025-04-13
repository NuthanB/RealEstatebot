# Multi-Agent Real Estate Chatbot

A Flask-based web application that implements a multi-agent chatbot system for real estate-related issues. The system consists of two specialized agents:

1. **Issue Detection & Troubleshooting Agent**: Processes property images to identify visible issues and provides troubleshooting suggestions.
2. **Tenancy FAQ Agent**: Answers frequently asked questions related to tenancy laws, agreements, and rental processes.

## Tools & Technologies Used

- **Backend Framework**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Models**: 
  - OpenAI's GPT-4 Vision API for image analysis
  - OpenAI's GPT-4 for tenancy question answering
- **Additional Libraries**: 
  - Requests for API calls
  - python-dotenv for environment variables

## How It Works

### Conversation Context
The system maintains conversation history to provide context-aware responses, especially for follow-up questions about uploaded images. This allows users to have ongoing discussions about property issues without uploading the same image multiple times.

### Agent Router
The system automatically identifies which agent should respond based on:
- Text classification (looking for tenancy-related keywords)
- Presence of an image (routes to the Issue Detection Agent)
- Previous conversation context (continues with the same agent for follow-ups)
- If unclear, it asks a clarifying question

### Issue Detection Agent
- Accepts user-uploaded images of properties
- Uses OpenAI's GPT-4 Vision to analyze the images
- Identifies visible issues like water damage, mold, cracks, etc.
- Provides troubleshooting suggestions and next steps
- Maintains context for follow-up questions about the same image

### Tenancy FAQ Agent
- Handles questions related to tenancy laws and agreements
- Provides location-specific guidance when possible
- Answers common questions about tenant/landlord responsibilities
- Maintains conversation context for multi-turn discussions

## Setup Instructions

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   SECRET_KEY=your_random_secret_key  # For session management
   ```
5. Run the application:
   ```
   python app.py
   ```
6. Open your browser and navigate to `http://localhost:5000`

## Usage Examples

### Issue Detection Example
1. Type a message like "What's wrong with this wall?"
2. Upload an image of the wall
3. The Issue Detection Agent will analyze the image and provide insights
4. Ask follow-up questions like "How can I fix it?" or "Is it dangerous?" without uploading the image again

### Tenancy FAQ Example
1. Type a question like "Can my landlord evict me without notice?"
2. The Tenancy FAQ Agent will provide information about eviction processes
3. Ask follow-up questions like "How much notice should they give?" to continue the conversation
4. For more specific information, include your location in the question

## Additional Information

- The chatbot UI automatically indicates which agent is currently active
- You can switch between agents by either uploading an image or asking a tenancy-related question
- For optimal results, provide clear images and specific questions
- The system maintains conversation context for a seamless experience

## Future Improvements

- Implement persistent storage for conversation history (database)
- Add support for multiple images in a single conversation
- Incorporate a database of location-specific tenancy laws
- Enhance the UI with more interactive features