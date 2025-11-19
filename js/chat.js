const API_BASE_URL = 'http://localhost:8000';
let currentChatId = null;
let authCredentials = null;
let currentUserId = null;

// Auth
function loadAuth() {
    const stored = localStorage.getItem('healthMonitorAuth');
    if (!stored) {
        window.location.href = '/';
        return false;
    }
    const auth = JSON.parse(stored);
    currentUserId = auth.userId;
    authCredentials = auth.credentials;
    return true;
}

async function authFetch(url, options = {}) {
    const headers = {
        'Authorization': 'Basic ' + btoa(authCredentials.username + ':' + authCredentials.password),
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    const response = await fetch(url, { ...options, headers });
    
    if (response.status === 401) {
        localStorage.removeItem('healthMonitorAuth');
        window.location.href = '/';
        return;
    }
    
    return response;
}

// Load chats
async function loadChats() {
    try {
        const response = await authFetch(`${API_BASE_URL}/api/chat/list`);
        const data = await response.json();
        
        const chatList = document.getElementById('chatList');
        if (data.chats && data.chats.length > 0) {
            chatList.innerHTML = data.chats.map(chat => `
                <div class="chat-item ${chat.chat_id === currentChatId ? 'active' : ''}" data-chat-id="${chat.chat_id}">
                    <div class="chat-item-content">
                        <h4>${escapeHtml(chat.chat_name)}</h4>
                        <p>${formatDate(chat.updated_at)}</p>
                    </div>
                    <button class="chat-item-delete" data-chat-id="${chat.chat_id}" title="Delete chat">
                        🗑️
                    </button>
                </div>
            `).join('');
            
            // Add click handlers for chat items
            document.querySelectorAll('.chat-item').forEach(item => {
                item.addEventListener('click', (e) => {
                    // Don't load chat if clicking delete button
                    if (!e.target.classList.contains('chat-item-delete')) {
                        loadChat(item.dataset.chatId);
                    }
                });
            });
            
            // Add click handlers for delete buttons
            document.querySelectorAll('.chat-item-delete').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    e.stopPropagation(); // Prevent chat from loading
                    const chatId = btn.dataset.chatId;
                    await deleteChatById(chatId);
                });
            });
        } else {
            chatList.innerHTML = '<p class="no-data">No chats yet. Create one to get started!</p>';
        }
    } catch (error) {
        console.error('Error loading chats:', error);
    }
}

// Load specific chat
async function loadChat(chatId) {
    try {
        const response = await authFetch(`${API_BASE_URL}/api/chat/${chatId}/messages`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.detail || 'Failed to load chat');
        }
        
        currentChatId = chatId;
        
        // Update UI
        document.getElementById('noChatSelected').classList.add('hidden');
        document.getElementById('chatContainer').classList.remove('hidden');
        
        // Update active chat in sidebar
        document.querySelectorAll('.chat-item').forEach(item => {
            item.classList.toggle('active', item.dataset.chatId === chatId);
        });
        
        // Get chat name
        const chatItem = document.querySelector(`.chat-item[data-chat-id="${chatId}"]`);
        if (chatItem) {
            const chatName = chatItem.querySelector('h4').textContent;
            document.getElementById('chatTitle').textContent = chatName;
        }
        
        // Display messages
        const messagesContainer = document.getElementById('chatMessages');
        if (data.messages && data.messages.length > 0) {
            messagesContainer.innerHTML = data.messages.map(msg => createMessageHTML(msg)).join('');
        } else {
            messagesContainer.innerHTML = '<p class="no-data">No messages yet. Start the conversation!</p>';
        }
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
    } catch (error) {
        console.error('Error loading chat:', error);
        alert('Failed to load chat: ' + error.message);
    }
}

// Create message HTML
function createMessageHTML(message) {
    const isUser = message.role === 'user';
    const time = new Date(message.created_at).toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit' 
    });
    
    // Render content based on role
    let contentHtml;
    if (isUser) {
        // User messages: simple text with line breaks
        contentHtml = escapeHtml(message.content).replace(/\n/g, '<br>');
    } else {
        // Assistant messages: render as markdown
        contentHtml = marked.parse(message.content);
    }
    
    return `
        <div class="message ${isUser ? 'message-user' : 'message-assistant'}">
            <div class="message-avatar">${isUser ? '👤' : '🤖'}</div>
            <div class="message-content">
                <div class="message-text">${contentHtml}</div>
                <div class="message-time">${time}</div>
            </div>
        </div>
    `;
}

// Send message
async function sendMessage(message, useHealthData, insightType = 'raw_data') {
    if (!currentChatId) return;
    
    const messagesContainer = document.getElementById('chatMessages');
    const sendBtn = document.getElementById('sendBtn');
    
    try {
        sendBtn.disabled = true;
        sendBtn.textContent = 'Sending...';
        
        // Add user message to UI immediately
        messagesContainer.innerHTML += createMessageHTML({
            role: 'user',
            content: message,
            created_at: new Date().toISOString()
        });
        
        // Add loading indicator
        messagesContainer.innerHTML += `
            <div class="message message-assistant" id="loadingMessage">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <div class="message-text">
                        <div class="typing-indicator">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        const response = await authFetch(`${API_BASE_URL}/api/chat/${currentChatId}/message`, {
            method: 'POST',
            body: JSON.stringify({
                message: message,
                use_health_data: useHealthData,
                insight_type: insightType
            })
        });
        
        const data = await response.json();
        
        // Remove loading indicator
        document.getElementById('loadingMessage')?.remove();
        
        if (data.success) {
            // Add AI response
            messagesContainer.innerHTML += createMessageHTML({
                role: 'assistant',
                content: data.response,
                created_at: new Date().toISOString()
            });
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // Reload chats to update timestamp
            loadChats();
        } else {
            throw new Error(data.error || 'Failed to send message');
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        document.getElementById('loadingMessage')?.remove();
        alert('Failed to send message: ' + error.message);
    } finally {
        sendBtn.disabled = false;
        sendBtn.textContent = 'Send';
    }
}

// Create new chat
async function createNewChat(chatName = null) {
    try {
        // Generate a default name if none provided
        if (!chatName) {
            const now = new Date();
            chatName = `Chat ${now.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} ${now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`;
        }
        
        const response = await authFetch(`${API_BASE_URL}/api/chat/new`, {
            method: 'POST',
            body: JSON.stringify({ chat_name: chatName })
        });
        
        const data = await response.json();
        
        if (data.success) {
            await loadChats();
            loadChat(data.chat_id);
        } else {
            throw new Error('Failed to create chat');
        }
    } catch (error) {
        console.error('Error creating chat:', error);
        alert('Failed to create chat: ' + error.message);
    }
}

// Delete chat
async function deleteChat() {
    if (!currentChatId) return;
    
    if (!confirm('Are you sure you want to delete this chat? This cannot be undone.')) {
        return;
    }
    
    await deleteChatById(currentChatId);
}

// Delete chat by ID
async function deleteChatById(chatId) {
    if (!chatId) return;
    
    if (!confirm('Are you sure you want to delete this chat? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await authFetch(`${API_BASE_URL}/api/chat/${chatId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            // If we're deleting the currently open chat, close it
            if (currentChatId === chatId) {
                currentChatId = null;
                document.getElementById('chatContainer').classList.add('hidden');
                document.getElementById('noChatSelected').classList.remove('hidden');
            }
            await loadChats();
        } else {
            throw new Error(data.detail || 'Failed to delete chat');
        }
    } catch (error) {
        console.error('Error deleting chat:', error);
        alert('Failed to delete chat: ' + error.message);
    }
}

// Rename chat
async function renameChat(newName) {
    if (!currentChatId) return;
    
    try {
        const response = await authFetch(`${API_BASE_URL}/api/chat/${currentChatId}/rename`, {
            method: 'PUT',
            body: JSON.stringify({ new_name: newName })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('chatTitle').textContent = newName;
            await loadChats();
            closeModal('renameChatModal');
        } else {
            throw new Error(data.detail || 'Failed to rename chat');
        }
    } catch (error) {
        console.error('Error renaming chat:', error);
        alert('Failed to rename chat: ' + error.message);
    }
}

// Modal helpers
function showModal(modalId) {
    document.getElementById(modalId).classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days} days ago`;
    
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    if (!loadAuth()) return;
    
    loadChats();
    
    // New chat button - directly create chat without modal
    document.getElementById('newChatBtn').addEventListener('click', () => {
        createNewChat();
    });
    
    document.getElementById('startNewChatBtn').addEventListener('click', () => {
        createNewChat();
    });
    
    // New chat form (kept for future use if needed)
    document.getElementById('newChatForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const chatName = document.getElementById('newChatName').value.trim();
        if (chatName) {
            createNewChat(chatName);
            document.getElementById('newChatName').value = '';
            closeModal('newChatModal');
        }
    });
    
    document.getElementById('cancelNewChat').addEventListener('click', () => {
        closeModal('newChatModal');
    });
    
    // Chat form
    document.getElementById('chatForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        const useHealthData = document.getElementById('useHealthData').checked;
        const insightType = document.getElementById('insightType').value;
        
        if (message && currentChatId) {
            input.value = '';
            input.style.height = 'auto';
            await sendMessage(message, useHealthData, insightType);
        }
    });
    
    // Toggle insight type selector based on checkbox
    document.getElementById('useHealthData').addEventListener('change', function() {
        document.getElementById('insightType').disabled = !this.checked;
    });
    
    // Auto-resize textarea
    document.getElementById('messageInput').addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
    
    // Delete chat
    document.getElementById('deleteChatBtn').addEventListener('click', deleteChat);
    
    // Rename chat
    document.getElementById('renameChatBtn').addEventListener('click', () => {
        const currentName = document.getElementById('chatTitle').textContent;
        document.getElementById('renameChatName').value = currentName;
        showModal('renameChatModal');
    });
    
    document.getElementById('renameChatForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const newName = document.getElementById('renameChatName').value.trim();
        if (newName) {
            renameChat(newName);
        }
    });
    
    document.getElementById('cancelRename').addEventListener('click', () => {
        closeModal('renameChatModal');
    });
    
    // Logout
    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('healthMonitorAuth');
        window.location.href = '/';
    });
    
    // Close modals when clicking outside
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(modal.id);
            }
        });
    });
});
