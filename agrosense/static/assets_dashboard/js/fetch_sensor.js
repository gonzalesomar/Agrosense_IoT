let humedadData = [
    { id: 'h1_sensor2', data: [1, 99] },
    { id: 'h2_sensor2', data: [40, 60] },
    { id: 'h3_sensor2', data: [20, 80] },
    { id: 'h1_sensor1', data: [56, 44] },
    { id: 'h2_sensor1', data: [48, 52] },
    { id: 'h3_sensor1', data: [25, 75] }
];
let charts = {}; // Object to store chart instances

// HUMEDAD
function createChartHumedad(elementId, data, backgroundColor = ['#2d9f21', '#f6f1f151']) {
    const ctx = document.getElementById(elementId).getContext('2d');
    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: data,
                backgroundColor: backgroundColor,
                borderColor: 'rgba(0, 0, 0, 0)'
            }],
            labels: ['Humidity', 'Remaining']
        },
        options: {
            responsive: true,
            maintainAspectRatio: true, 
            cutout: '70%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        },
        plugins: [{
            afterDraw: function(chart) {
                if (chart.data.datasets && chart.data.datasets[0]) {
                    const ctx = chart.ctx;
                    const value = chart.data.datasets[0].data[0];
                    const cx = chart.chartArea.left + chart.chartArea.width / 2;
                    const cy = chart.chartArea.top + chart.chartArea.height / 2;
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.font = '20px Arial';
                    ctx.fillStyle = 'black';
                    ctx.fillText(value + '%', cx, cy);
                }
            }
        }],
    });

    ctx.canvas.addEventListener('mouseenter', () => {
        chart.data.datasets[0].backgroundColor = ['#ff5722', '#f6f1f151'];
        chart.update();
    });

    ctx.canvas.addEventListener('mouseleave', () => {
        chart.data.datasets[0].backgroundColor = backgroundColor;
        chart.update();
    });
    charts[elementId] = chart;
    return chart;
}
// Actualizar datos de los sensores de humedad
function updateSensorData(sensorId, humidityKey, data, humedadData, charts) {
    const sensorIndex = humedadData.findIndex(sensor => sensor.id === sensorId);
    if (sensorIndex !== -1) {
        const humidityValue = parseFloat(data[humidityKey]);
        humedadData[sensorIndex].data = [humidityValue, 100 - humidityValue];
        console.log(sensorId, humedadData[sensorIndex].data);
        const chart = charts[sensorId];
        if (chart) {
            chart.data.datasets[0].data = [humidityValue, 100 - humidityValue];
            chart.update();
        }
    }
}
// CALENDARIO
document.addEventListener('DOMContentLoaded', function() {
    let selectedDate = null; // Variable to store the selected date

    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        dateClick: function(info) {
            selectedDate = info.dateStr; // Save the clicked date
            // alert('Selected date: ' + selectedDate);
        }
    });
    calendar.render();
});

// FETCH SENSOR DATA
document.addEventListener("DOMContentLoaded", function() {
    function fetchSensorData() {
      fetch('/get-sensor-data/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('battery-level').textContent = data.battery_level_1;
            console.log('battery-level element:', document.getElementById('battery-level'));

            document.getElementById('battery-level-2').textContent = data.battery_level_2;
            console.log('battery-level-2 element:', document.getElementById('battery-level-2'));

            updateSensorData('h1_sensor1', 'humidity_25_1', data, humedadData, charts);
            updateSensorData('h2_sensor1', 'humidity_50_1', data, humedadData, charts);
            updateSensorData('h3_sensor1', 'humidity_75_1', data, humedadData, charts);
            updateSensorData('h1_sensor2', 'humidity_25_2', data, humedadData, charts);
            updateSensorData('h2_sensor2', 'humidity_50_2', data, humedadData, charts);
            updateSensorData('h3_sensor2', 'humidity_75_2', data, humedadData, charts);

            document.getElementById('electrical-conductivity').textContent = data.electrical_conductivity_1;
            console.log('electrical-conductivity element', document.getElementById('electrical-conductivity'));
            document.getElementById('electrical-conductivity-2').textContent = data.electrical_conductivity_2;
            console.log('electrical-conductivity-2 element', document.getElementById('electrical-conductivity-2'));
        })
        .catch(error => console.error('Error fetching sensor data:', error));
    }
    // Fetch the sensor data immediately and then every 60 seconds
    fetchSensorData();
    console.log('Humedad_data: ', humedadData);
    humedadData.forEach(h => createChartHumedad(h.id, h.data));
    setInterval(fetchSensorData, 60000);
  });