document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('projects').addEventListener('change', function() {
        if (this.value === 'sensor1') {
            document.querySelector('.chart_1').style.display = 'flex';
            document.querySelector('.chart_2').style.display = 'none';
        } else if (this.value === 'sensor2') {
            document.querySelector('.chart_1').style.display = 'none';
            document.querySelector('.chart_2').style.display = 'flex';
        }
    });
});