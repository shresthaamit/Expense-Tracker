new Chart($("#barChartID"), { 
    type: 'pie', 
    options: { 
        legend: { display: true }, 
        indexAxis: 'x', 
        title: { 
            display: true, 
            text: 'pie Chart using ChartJS library' 
        } 
    }, 
    data: { 
       
        datasets: [ 
            { 
                label: "Technology Learned by Students", 
                backgroundColor: ["#FFC0CB", "#0000FF", 
                    "#00FFFF",], 
                data: [234, 356, 819] 
            } 
        ], 
        labels: ["C++", "Java", "Blockchain"]
    }             
}); 
