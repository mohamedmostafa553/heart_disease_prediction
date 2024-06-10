document.getElementById('predictionForm').addEventListener('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.textContent = 'Error: ' + data.error;
            resultDiv.style.color = 'red';
        } else {
            resultDiv.textContent = 'Prediction: ' + data.prediction;
            resultDiv.style.color = 'green';
        }
    })
    .catch(error => {
        let resultDiv = document.getElementById('result');
        resultDiv.textContent = 'Error: ' + error.message;
        resultDiv.style.color = 'red';
    });
});
