/**
 * DACTE PDF Extractor - Frontend Logic
 * Handles drag-drop upload, extraction preview, and Excel download
 */

document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const fileItems = document.getElementById('fileItems');
    const clearFiles = document.getElementById('clearFiles');
    const processBtn = document.getElementById('processBtn');
    const uploadCard = document.getElementById('uploadCard');
    const processingCard = document.getElementById('processingCard');
    const resultsCard = document.getElementById('resultsCard');
    const errorCard = document.getElementById('errorCard');
    const previewBody = document.getElementById('previewBody');
    const resultsSummary = document.getElementById('resultsSummary');
    const downloadBtn = document.getElementById('downloadBtn');
    const newUploadBtn = document.getElementById('newUploadBtn');
    const retryBtn = document.getElementById('retryBtn');
    const processingStatus = document.getElementById('processingStatus');
    const errorMessage = document.getElementById('errorMessage');

    let selectedFiles = [];
    let extractedData = null;

    // ============================
    // Drag & Drop Handlers
    // ============================

    uploadZone.addEventListener('click', () => fileInput.click());

    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.remove('dragover');
        
        const files = Array.from(e.dataTransfer.files).filter(f => f.name.toLowerCase().endsWith('.pdf'));
        if (files.length === 0) {
            showError('Apenas arquivos PDF são aceitos.');
            return;
        }
        addFiles(files);
    });

    fileInput.addEventListener('change', (e) => {
        const files = Array.from(e.target.files);
        addFiles(files);
        fileInput.value = '';
    });

    // ============================
    // File Management
    // ============================

    function addFiles(files) {
        selectedFiles = [...selectedFiles, ...files];
        renderFileList();
    }

    function renderFileList() {
        if (selectedFiles.length === 0) {
            fileList.style.display = 'none';
            return;
        }

        fileList.style.display = 'block';
        fileItems.innerHTML = '';

        selectedFiles.forEach((file, idx) => {
            const li = document.createElement('li');
            const size = formatFileSize(file.size);
            li.innerHTML = `
                <span class="file-name">${file.name}</span>
                <span class="file-size">${size}</span>
            `;
            fileItems.appendChild(li);
        });
    }

    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }

    clearFiles.addEventListener('click', () => {
        selectedFiles = [];
        renderFileList();
    });

    // ============================
    // Process & Upload
    // ============================

    processBtn.addEventListener('click', async () => {
        if (selectedFiles.length === 0) return;

        showCard('processing');
        processingStatus.textContent = `Processando ${selectedFiles.length} arquivo(s)...`;

        const formData = new FormData();
        selectedFiles.forEach(file => formData.append('files', file));

        try {
            // First, get preview data
            processingStatus.textContent = 'Extraindo dados dos PDFs...';
            
            const previewResponse = await fetch('/extract', {
                method: 'POST',
                body: formData
            });

            if (!previewResponse.ok) {
                const err = await previewResponse.json();
                throw new Error(err.error || 'Erro ao processar PDFs');
            }

            const previewData = await previewResponse.json();
            extractedData = previewData;

            if (previewData.count === 0) {
                throw new Error('Nenhum DACTE encontrado nos PDFs enviados.');
            }

            // Show results
            renderResults(previewData);
            showCard('results');

        } catch (err) {
            showError(err.message);
        }
    });

    // ============================
    // Results Display
    // ============================

    function renderResults(data) {
        resultsSummary.textContent = `${data.count} DACTE(s) extraído(s) com sucesso`;
        
        if (data.errors && data.errors.length > 0) {
            resultsSummary.textContent += ` (${data.errors.length} erro(s))`;
        }

        previewBody.innerHTML = '';
        data.data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.cte}</td>
                <td>${row.tipo || ''}</td>
                <td>${row.data_emissao || ''}</td>
                <td>${row.planta || ''}</td>
                <td class="valor-cell">${formatCurrency(row.valor)}</td>
                <td class="valor-cell">${formatCurrency(row.valor_servico)}</td>
                <td>${row.conteiner || 'N/A'}</td>
            `;
            previewBody.appendChild(tr);
        });
    }

    function formatCurrency(value) {
        if (!value && value !== 0) return '';
        return 'R$ ' + Number(value).toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    // ============================
    // Download Excel
    // ============================

    downloadBtn.addEventListener('click', async () => {
        if (selectedFiles.length === 0) return;

        downloadBtn.disabled = true;
        downloadBtn.innerHTML = `
            <div class="spinner" style="width:18px;height:18px;border-width:2px;"></div>
            Gerando Excel...
        `;

        const formData = new FormData();
        selectedFiles.forEach(file => formData.append('files', file));

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.error || 'Erro ao gerar Excel');
            }

            // Get filename from Content-Disposition header
            const disposition = response.headers.get('Content-Disposition');
            let filename = 'DACTE_Extraidos.xlsx';
            if (disposition) {
                const match = disposition.match(/filename=(.+)/);
                if (match) filename = match[1].replace(/"/g, '');
            }

            // Download the file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

        } catch (err) {
            showError(err.message);
        } finally {
            downloadBtn.disabled = false;
            downloadBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M10 2V14M10 14L5 9M10 14L15 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M3 14V16C3 17.1046 3.89543 18 5 18H15C16.1046 18 17 17.1046 17 16V14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Baixar Excel
            `;
        }
    });

    // ============================
    // Card Visibility
    // ============================

    function showCard(card) {
        uploadCard.style.display = card === 'upload' ? 'block' : 'none';
        processingCard.style.display = card === 'processing' ? 'block' : 'none';
        resultsCard.style.display = card === 'results' ? 'block' : 'none';
        errorCard.style.display = card === 'error' ? 'block' : 'none';
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        showCard('error');
    }

    // ============================
    // Navigation
    // ============================

    newUploadBtn.addEventListener('click', () => {
        selectedFiles = [];
        extractedData = null;
        renderFileList();
        showCard('upload');
    });

    retryBtn.addEventListener('click', () => {
        showCard('upload');
    });
});
