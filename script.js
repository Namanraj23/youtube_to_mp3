const playlistUrlInput = document.getElementById('playlist-url');
const convertBtn = document.getElementById('convert-btn');
const outputDiv = document.getElementById('output');
const progressBar = document.getElementById('progress');
const progressText = document.getElementById('progress-text');

convertBtn.addEventListener('click', async () => {
  const playlistUrl = playlistUrlInput.value.trim();
  if (!playlistUrl) {
    alert('Please enter a valid YouTube playlist URL');
    return;
  }

  try {
    const response = await fetch('/convert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ playlistUrl }),
    });

    const result = await response.json();
    outputDiv.innerText = result.message;

    // Update the progress bar
    const progressInterval = setInterval(async () => {
      const progressResponse = await fetch('/progress');
      const progressData = await progressResponse.json();
      const progressValue = progressData.progress;
      progressBar.value = progressValue;
      progressText.innerText = `${progressValue}%`;
      if (progressValue === 100) {
        clearInterval(progressInterval);
      }
    }, 1000); // Update every 1 second
  } catch (error) {
    console.error(error);
    outputDiv.innerText = 'Error converting playlist to MP3';
  }
});