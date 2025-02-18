document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('video-input');
    const file = fileInput.files[0];
    if (!file) return;
    
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const resultMessage = document.getElementById('result-message');
    const confidence = document.getElementById('confidence');
    
    loading.classList.remove('hidden');
    result.classList.add('hidden');
    
    const formData = new FormData();
    formData.append('video', file);
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultMessage.textContent = `Error: ${data.error}`;
            confidence.textContent = '';
        } else {
            resultMessage.textContent = data.message;
            confidence.textContent = `Confidence: ${data.confidence.toFixed(2)}%`;
            result.className = data.is_deepfake ? 'deepfake' : 'genuine';
        }
    } catch (error) {
        resultMessage.textContent = 'An error occurred during analysis';
        confidence.textContent = '';
    } finally {
        loading.classList.add('hidden');
        result.classList.remove('hidden');
    }
});

