const API_BASE_URL = 'http://localhost:8000';
let authCredentials = null;

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    setTimeout(() => errorDiv.classList.add('hidden'), 5000);
}

function showSuccess(message) {
    const successDiv = document.getElementById('success');
    successDiv.textContent = message;
    successDiv.classList.remove('hidden');
    setTimeout(() => successDiv.classList.add('hidden'), 5000);
}

function showProgress(show, text = 'Uploading...') {
    const progressDiv = document.getElementById('uploadProgress');
    const progressText = document.getElementById('progressText');
    progressDiv.classList.toggle('hidden', !show);
    if (text) {
        progressText.textContent = text;
    }
}

// Check authentication
function checkAuth() {
    const stored = localStorage.getItem('healthMonitorAuth');
    if (!stored) {
        window.location.href = '/';
        return null;
    }
    const auth = JSON.parse(stored);
    authCredentials = auth.credentials;
    return auth;
}

// Load user info
async function loadUserInfo() {
    const auth = checkAuth();
    if (!auth) return;
    
    document.getElementById('userInfo').textContent = `Logged in as: ${auth.credentials.username}`;
}

// Logout
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('healthMonitorAuth');
    window.location.href = '/';
});

// File input handling
const fileInput = document.getElementById('fileInput');
const fileDropArea = document.getElementById('fileDropArea');
const fileName = document.getElementById('fileName');
const uploadBtn = document.getElementById('uploadBtn');

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        fileName.textContent = file.name;
        uploadBtn.disabled = false;
    } else {
        fileName.textContent = '';
        uploadBtn.disabled = true;
    }
});

// Drag and drop
fileDropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileDropArea.classList.add('drag-over');
});

fileDropArea.addEventListener('dragleave', () => {
    fileDropArea.classList.remove('drag-over');
});

fileDropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileDropArea.classList.remove('drag-over');
    
    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith('.zip')) {
        fileInput.files = e.dataTransfer.files;
        fileName.textContent = file.name;
        uploadBtn.disabled = false;
    } else {
        showError('Please drop a ZIP file');
    }
});

// Upload form submission
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const file = fileInput.files[0];
    if (!file) {
        showError('Please select a file');
        return;
    }
    
    if (!file.name.endsWith('.zip')) {
        showError('Only ZIP files are allowed');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        uploadBtn.disabled = true;
        showProgress(true, 'Uploading and processing...');
        
        const response = await fetch(`${API_BASE_URL}/api/upload`, {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa(authCredentials.username + ':' + authCredentials.password)
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Upload failed');
        }
        
        showProgress(false);
        showSuccess('Health data imported successfully! Redirecting to dashboard...');
        
        // Clear form
        fileInput.value = '';
        fileName.textContent = '';
        uploadBtn.disabled = true;
        
        // Redirect to dashboard after 2 seconds
        setTimeout(() => {
            window.location.href = '/dashboard';
        }, 2000);
        
    } catch (error) {
        showProgress(false);
        showError(error.message);
        uploadBtn.disabled = false;
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadUserInfo();
});
