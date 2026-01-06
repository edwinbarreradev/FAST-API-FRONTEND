const API_URL = "http://127.0.0.1:8000/peliculas/";

// Función para obtener películas y actualizar todo
async function obtenerPeliculas() {
    try {
        const respuesta = await fetch(API_URL);
        const peliculas = await respuesta.json();

        // Actualizar la lista
        const listaPeliculas = document.getElementById("lista-peliculas");
        listaPeliculas.innerHTML = "";

        peliculas.forEach(pelicula => {
            const li = document.createElement("li");
    // Crear contenedor para el texto (para evitar que se rompa)
    const texto = document.createElement("span");
    texto.textContent = `${pelicula.titulo} - ${pelicula.director} (${pelicula.anio})`;
    li.appendChild(texto);

    // Botón Editar
    const btnEditar = document.createElement("button");
    btnEditar.innerHTML = '<i class="fas fa-edit"></i> Editar';
    btnEditar.onclick = () => editarPelicula(pelicula);
    li.appendChild(btnEditar);

    // Botón Eliminar
    const btnEliminar = document.createElement("button");
    btnEliminar.innerHTML = '<i class="fas fa-trash-alt"></i> Eliminar';
    btnEliminar.onclick = () => eliminarPelicula(pelicula.id);
    li.appendChild(btnEliminar);

    listaPeliculas.appendChild(li)
        });

        // Actualizar dashboard y slider con los datos obtenidos
        actualizarDashboard(peliculas);
        actualizarSlider(peliculas);

    } catch (error) {
        console.error("Error al obtener películas:", error);
    }
}

async function agregarPelicula(event) {
    event.preventDefault();
    const titulo = document.getElementById("titulo").value;
    const director = document.getElementById("director").value;
    const anio = document.getElementById("anio").value;
    const pelicula_id = document.getElementById("pelicula_id").value;
    const method = pelicula_id ? "PUT" : "POST";
    const url = pelicula_id ? API_URL + pelicula_id + "/" : API_URL;

    const respuesta = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ titulo, director, anio })
    });

    if (respuesta.ok) {
        obtenerPeliculas();
        limpiarFormulario();
    }
}

function editarPelicula(pelicula) {
    document.getElementById("titulo").value = pelicula.titulo;
    document.getElementById("director").value = pelicula.director;
    document.getElementById("anio").value = pelicula.anio;
    document.getElementById("pelicula_id").value = pelicula.id;
    document.querySelector("button[type='submit']").textContent = "Actualizar Película";
}

async function eliminarPelicula(pelicula_id) {
    const respuesta = await fetch(API_URL + pelicula_id + "/", {
        method: "DELETE"
    });
    if (respuesta.ok) {
        obtenerPeliculas();
    }
}

function limpiarFormulario() {
    document.getElementById("titulo").value = "";
    document.getElementById("director").value = "";
    document.getElementById("anio").value = "";
    document.getElementById("pelicula_id").value = "";
    document.querySelector("button[type='submit']").textContent = "Agregar Película";
}

// NUEVA FUNCIÓN: Actualizar el dashboard con estadísticas reales
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

// NUEVA FUNCIÓN: Actualizar el slider con películas reales
function actualizarSlider(peliculas) {
    const slider = document.querySelector('.slider');
    slider.innerHTML = '';

    peliculas.forEach(pelicula => {
        const slide = document.createElement('div');
        slide.classList.add('slide');

        // Imagen por defecto si no tienes imágenes en la API
        const imgSrc = pelicula.imagen || `https://source.unsplash.com/300x450/?movie,${encodeURIComponent(pelicula.titulo)}`;
        slide.innerHTML = `
            <img src="${imgSrc}" alt="${pelicula.titulo}">
            <h3>${pelicula.titulo}</h3>
            <p>${pelicula.anio} | ${pelicula.director}</p>
        `;

        slider.appendChild(slide);
    });
}

document.getElementById("formulario-pelicula").addEventListener("submit", agregarPelicula);
obtenerPeliculas();