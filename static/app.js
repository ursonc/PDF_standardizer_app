document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const uploadForm = document.getElementById('uploadForm');
    const pdfFileInput = document.getElementById('pdfFile');
    const fileName = document.getElementById('fileName');
    const presetSizeSelect = document.getElementById('presetSize');
    const customSizeFields = document.getElementById('customSizeFields');
    const widthInput = document.getElementById('width');
    const heightInput = document.getElementById('height');
    const convertBtn = document.getElementById('convertBtn');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const statusMessage = document.getElementById('statusMessage');
    const resultContainer = document.getElementById('resultContainer');
    const downloadLink = document.getElementById('downloadLink');
    const newConversionBtn = document.getElementById('newConversionBtn');
    const dropArea = document.getElementById('dropArea');
    const browseBtn = document.getElementById('browseBtn');

    // Page size presets in points
    const presets = {
        'a4': { width: 595, height: 842 },
        'letter': { width: 612, height: 792 },
        'legal': { width: 612, height: 1008 },
        'custom': null
    };

    // File input change handler
    pdfFileInput.addEventListener('change', (e) => {
        handleFileSelection(e.target.files[0]);
    });

    // Handle file selection (used by both input change and drop events)
    function handleFileSelection(file) {
        if (file) {
            fileName.textContent = file.name;
            convertBtn.disabled = false;
        } else {
            fileName.textContent = 'No file selected';
            convertBtn.disabled = true;
        }
    }

    // File input click event delegation
    document.querySelector('.file-input-container').addEventListener('click', () => {
        pdfFileInput.click();
    });

    // Browse button click
    browseBtn.addEventListener('click', () => {
        pdfFileInput.click();
    });

    // Drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropArea.classList.add('active');
    }
    
    function unhighlight() {
        dropArea.classList.remove('active');
    }
    
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const file = dt.files[0];
        
        if (file && file.type === 'application/pdf') {
            pdfFileInput.files = dt.files;
            handleFileSelection(file);
        } else if (file) {
            alert('Please drop a PDF file.');
        }
    }

    // Preset size change handler
    presetSizeSelect.addEventListener('change', () => {
        const selectedPreset = presetSizeSelect.value;
        
        if (selectedPreset === 'custom') {
            customSizeFields.classList.remove('hidden');
        } else {
            customSizeFields.classList.add('hidden');
            const preset = presets[selectedPreset];
            widthInput.value = preset.width;
            heightInput.value = preset.height;
        }
    });

    // Form submission
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        const file = pdfFileInput.files[0];
        
        if (!file) {
            alert('Please select a PDF file.');
            return;
        }
        
        formData.append('pdfFile', file);
        formData.append('width', widthInput.value);
        formData.append('height', heightInput.value);
        
        // UI state: processing
        uploadForm.classList.add('hidden');
        progressContainer.classList.remove('hidden');
        resultContainer.classList.add('hidden');
        
        try {
            // Simulate progress (since we don't have real-time progress updates from server)
            const progressInterval = simulateProgress();
            
            // Submit the form
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            // Clear progress simulation
            clearInterval(progressInterval);
            progressBar.style.width = '100%';
            
            const result = await response.json();
            
            if (response.ok) {
                // Success state
                downloadLink.href = `/download/${result.filename}`;
                progressContainer.classList.add('hidden');
                resultContainer.classList.remove('hidden');
            } else {
                // Error state
                throw new Error(result.error || 'Failed to convert PDF');
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
            resetUI();
        }
    });
    
    // New conversion button handler
    newConversionBtn.addEventListener('click', resetUI);
    
    // Helper Functions
    function resetUI() {
        uploadForm.classList.remove('hidden');
        progressContainer.classList.add('hidden');
        resultContainer.classList.add('hidden');
        progressBar.style.width = '0%';
        fileName.textContent = 'No file selected';
        pdfFileInput.value = '';
        convertBtn.disabled = true;
        presetSizeSelect.value = 'a4';
        widthInput.value = presets.a4.width;
        heightInput.value = presets.a4.height;
        customSizeFields.classList.add('hidden');
        // Reset drag area highlight if any
        dropArea.classList.remove('active');
    }
    
    function simulateProgress() {
        let progress = 0;
        
        return setInterval(() => {
            if (progress < 95) {
                progress += Math.random() * 5;
                progressBar.style.width = `${progress}%`;
            }
        }, 300);
    }
}); 