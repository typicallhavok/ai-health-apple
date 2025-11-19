const API_BASE_URL = 'http://localhost:8000';

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    setTimeout(() => errorDiv.classList.add('hidden'), 5000);
}

// Login form
document.getElementById('loginFormElement').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/login`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }
        
        // Store credentials for future requests
        const auth = {
            userId: data.user_id,
            credentials: {
                username: formData.get('username'),
                password: formData.get('password')
            }
        };
        localStorage.setItem('healthMonitorAuth', JSON.stringify(auth));
        
        // Redirect to upload page
        window.location.href = '/upload';
        
    } catch (error) {
        showError(error.message);
    }
});

// Check if already logged in
if (localStorage.getItem('healthMonitorAuth')) {
    window.location.href = '/upload';
}
