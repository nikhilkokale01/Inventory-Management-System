// Sample analytics data
const analyticsData = {
    labels: ['Visitors', 'Page Views', 'Clicks', 'Conversions'],
    datasets: [{
        label: 'Analytics Data',
        data: [1000, 5000, 300, 25],
        backgroundColor: [
            'rgba(75, 192, 192, 0.2)',
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(54, 162, 235, 0.2)'
        ],
        borderColor: [
            'rgba(75, 192, 192, 1)',
            'rgba(255, 99, 132, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(54, 162, 235, 1)'
        ],
        borderWidth: 1
    }]
};

// Get the canvas element
const ctx = document.getElementById('barChart').getContext('2d');

// Create a bar chart
const barChart = new Chart(ctx, {
    type: 'bar',
    data: analyticsData,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
