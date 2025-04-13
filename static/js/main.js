document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const imageInput = document.getElementById('image-input');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeImageButton = document.getElementById('remove-image');
    const issueAgentIndicator = document.getElementById('issue-agent-indicator');
    const tenancyAgentIndicator = document.getElementById('tenancy-agent-indicator');
    
    let uploadedImage = null;
    
    // Store conversation history
    let conversationHistory = [];
    
    // Handle file selection for image upload
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file && file.type.match('image.*')) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                uploadedImage = e.target.result;
                imagePreview.src = uploadedImage;
                imagePreviewContainer.style.display = 'block';
            };
            
            reader.readAsDataURL(file);
        }
    });
    
    // Remove selected image
    removeImageButton.addEventListener('click', function() {
        uploadedImage = null;
        imagePreview.src = '';
        imagePreviewContainer.style.display = 'none';
        imageInput.value = '';
    });
    
    // Handle chat form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        
        // Don't send empty messages (unless there's an image)
        if (!message && !uploadedImage) return;
        
        // Create user message object
        const userMessage = {
            message: message,
            image: uploadedImage,
            sender: 'user',
            timestamp: new Date().toISOString()
        };
        
        // Add user message to chat
        addMessageToUI('user', message, uploadedImage);
        
        // Add to conversation history
        conversationHistory.push(userMessage);
        
        // Clear input
        userInput.value = '';
        
        // Add loading indicator
        const loadingMsgElement = addMessageToUI('bot', 'Thinking...');
        
        // Prepare data for sending to backend
        const requestData = {
            message: message,
            conversation_history: conversationHistory
        };
        
        if (uploadedImage) {
            requestData.image = uploadedImage;
        }
        
        // Make API request
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message
            loadingMsgElement.remove();
            
            // Create bot message object
            const botMessage = {
                message: data.response,
                sender: 'bot',
                agent: data.agent,
                message_id: data.message_id,
                timestamp: new Date().toISOString()
            };
            
            // Add bot response to UI
            addMessageToUI('bot', data.response);
            
            // Add to conversation history
            conversationHistory.push(botMessage);
            
            // Highlight active agent
            updateAgentIndicator(data.agent);
            
            // Reset image upload after sending
            if (uploadedImage) {
                uploadedImage = null;
                imagePreview.src = '';
                imagePreviewContainer.style.display = 'none';
                imageInput.value = '';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            loadingMsgElement.remove();
            addMessageToUI('bot', 'Sorry, there was an error processing your request.');
        });
    });
    
    // Add a message to the chat UI
    function addMessageToUI(sender, text, image = null) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        
        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        contentElement.textContent = text;
        messageElement.appendChild(contentElement);
        
        // Add image if provided
        if (image && sender === 'user') {
            const imgElement = document.createElement('img');
            imgElement.src = image;
            imgElement.classList.add('message-image');
            contentElement.appendChild(imgElement);
        }
        
        chatMessages.appendChild(messageElement);
        
        // Scroll to the bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return messageElement;
    }
    
    // Update agent indicator
    function updateAgentIndicator(agent) {
        issueAgentIndicator.classList.remove('active');
        tenancyAgentIndicator.classList.remove('active');
        
        // if (agent === 'issue_agent') {
        //     issueAgentIndicator.classList.add('active');
        // } else if (agent === 'tenancy_agent') {
        //     tenancyAgentIndicator.classList.add('active');
        // }
    }
});