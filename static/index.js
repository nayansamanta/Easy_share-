function showTab(tab) {
    document.getElementById('share').classList.add('hidden');
    document.getElementById('view').classList.add('hidden');
    document.getElementById('shareTab').classList.remove('active');
    document.getElementById('viewTab').classList.remove('active');

    document.getElementById(tab).classList.remove('hidden');
    document.getElementById(tab + 'Tab').classList.add('active');
}

async function shareFile() {
    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files.length) {
        alert("Please select a file to share.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/share', { method: 'POST', body: formData });
        const result = await response.json();
        if (response.ok) {
            document.getElementById('shareResult').innerHTML = `File shared! Access URL: <a href="${result.access_url}" target="_blank">${result.access_url}</a>`;
        } else {
            document.getElementById('shareResult').innerText = `Error: ${result.error}`;
        }
    } catch (error) {
        document.getElementById('shareResult').innerText = `Error sharing file: ${error}`;
    }
}

async function viewFile() {
    const token = document.getElementById('tokenInput').value;
    if (!token) {
        alert("Please enter a token.");
        return;
    }

    document.getElementById('viewResult').innerHTML = `<iframe src="/view/${token}" width="100%" height="600px"></iframe>`;
}
