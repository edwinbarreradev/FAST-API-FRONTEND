const API_URL = "http://127.0.0.1:8000/peliculas/";

// Cargar datos y gráficos
window.onload = async () => {
    try {
        const respuesta = await fetch(API_URL);
        const peliculas = await respuesta.json();

        // Actualizar dashboard
        actualizarDashboard(peliculas);

        // Actualizar tabla
        actualizarTabla(peliculas);

        // Generar gráficos
        crearGraficoAnio(peliculas);
        crearGraficoDirector(peliculas);

    } catch (error) {
        console.error("Error al cargar datos:", error);
    }
};

function actualizarDashboard(peliculas) {
    const total = peliculas.length;
    const directores = [...new Set(peliculas.map(p => p.director))].length;
    const anios = peliculas.map(p => p.anio);
    const ultimoAno = Math.max(...anios);
    const promedioAno = total > 0 ? (anios.reduce((a, b) => a + b, 0) / total).toFixed(1) : 0;

    document.getElementById('total-peliculas').textContent = total;
    document.getElementById('total-directores').textContent = directores;
    document.getElementById('ultimo-ano').textContent = ultimoAno || '-';
    document.getElementById('promedio-ano').textContent = promedioAno;
}

function actualizarTabla(peliculas) {
    const tbody = document.querySelector('#tabla-peliculas tbody');
    tbody.innerHTML = '';

    peliculas.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.id}</td>
            <td>${p.titulo}</td>
            <td>${p.director}</td>
            <td>${p.anio}</td>
        `;
        tbody.appendChild(tr);
    });
}

function crearGraficoAnio(peliculas) {
    const ctx = document.getElementById('anioChart').getContext('2d');

    const anios = peliculas.map(p => p.anio);
    const labels = anios;
    const data = anios;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Año de Película',
                data: data,
                backgroundColor: 'rgba(52, 152, 219, 0.6)',
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function crearGraficoDirector(peliculas) {
    const ctx = document.getElementById('directorChart').getContext('2d');

    const conteo = {};
    peliculas.forEach(p => {
        conteo[p.director] = (conteo[p.director] || 0) + 1;
    });

    const labels = Object.keys(conteo);
    const data = Object.values(conteo);

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#3498db',
                    '#e74c3c',
                    '#2ecc71',
                    '#f39c12',
                    '#9b59b6',
                    '#1abc9c',
                    '#e67e22'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#fff'
                    }
                }
            }
        }
    });
}