let chart = null;
let currentStep = 1;

const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const loadingModal = document.getElementById('loadingModal');

function updateLoadingStep() {
    document.querySelectorAll('.step').forEach((step, index) => {
        step.classList.toggle('active', index + 1 <= currentStep);
    });
    currentStep = currentStep % 3 + 1;
}

function showLoadingModal() {
    loadingModal.style.display = 'block';
    currentStep = 1;
    const stepInterval = setInterval(updateLoadingStep, 1000);
    return stepInterval;
}

function hideLoadingModal() {
    loadingModal.style.display = 'none';
}

// ... Resto del código de eventos del dropZone y fileInput ...
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.transform = 'scale(1.02)';
});

dropZone.addEventListener('dragleave', () => {
    dropZone.style.transform = 'scale(1)';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.transform = 'scale(1)';
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        processImage(file);
    }
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        processImage(file);
    }
});

function processImage(file) {
  const reader = new FileReader();
  reader.onload = async function (e) {
      // Mostrar la vista previa de la imagen
      document.getElementById('previewImage').src = e.target.result;
      document.getElementById('results').style.display = 'none';
      // Mostrar el modal de carga simulado
      const stepInterval = showLoadingModal();

      try {
          // Preparar los datos para enviar al backend
          const formData = new FormData();
          formData.append('file', file);
          // Realizar la llamada al backend
          const response = await fetch('http://127.0.0.1:8000/process-image/', {
              method: 'POST',
              body: formData,
          });

          // Obtener los resultados del backend
          const results = await response.json();
          // Detener el modal de carga y mostrar los resultados
          clearInterval(stepInterval);
          hideLoadingModal();
          showResults(results.predict);
      } catch (error) {
          // Manejo de errores
          clearInterval(stepInterval);
          hideLoadingModal();
          alert('Ocurrió un error al procesar la imagen. Por favor, inténtalo de nuevo.');
      }
  };

  // Leer la imagen como DataURL para previsualizarla
  reader.readAsDataURL(file);
}

// ... Resto del código de showResults y eventos ...

function showResults(results) {
  document.getElementById('loading').style.display = 'none';
  document.getElementById('results').style.display = 'block';

  if (chart) {
      chart.destroy();
  }

  const ctx = document.getElementById('resultsChart').getContext('2d');
  chart = new Chart(ctx, {
      type: 'pie',
      data: {
          labels: ['Glioma', 'Meningioma', 'Sin Tumor', 'Pituitaria'],
          datasets: [{
              data: [
                  results.glioma * 100,
                  results.meningioma * 100,
                  results.notumor * 100,
                  results.pituitary * 100
              ],
              backgroundColor: [
                  '#f87171',
                  '#60a5fa',
                  '#4ade80',
                  '#c084fc'
              ],
              borderWidth: 2,
              borderColor: '#1e293b'
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'bottom',
                  labels: {
                      color: '#f1f5f9',
                      padding: 20,
                      font: {
                          size: 14,
                          family: "'Inter', sans-serif"
                      }
                  }
              },
              tooltip: {
                  callbacks: {
                      label: function(context) {
                          return `${context.label}: ${context.raw.toFixed(2)}%`;
                      }
                  },
                  padding: 12,
                  bodyFont: {
                      size: 14,
                      family: "'Inter', sans-serif"
                  }
              }
          }
      }
  });

  // Generar mensaje de diagnóstico
  const diagnosisMessage = document.getElementById('diagnosisMessage');
  const maxEntry = Object.entries(results).reduce((a, b) => 
      a[1] > b[1] ? a : b
  );
  const maxCategory = maxEntry[0];
  const percentage = (maxEntry[1] * 100).toFixed(2);

  if (maxCategory === 'notumor') {
      diagnosisMessage.innerHTML = `La imagen analizada no muestra signos de tumor con un ${percentage}% de probabilidad.`;
      diagnosisMessage.className = 'diagnosis-message success';
  } else {
      diagnosisMessage.innerHTML = `La imagen analizada muestra un ${percentage}% de probabilidad de tumor tipo ${maxCategory}.`;
      diagnosisMessage.className = 'diagnosis-message warning';
  }
}