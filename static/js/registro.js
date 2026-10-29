/*
@ Autor: Jhon Esteban Garcia Florez
@ fecha: 06/09/2026
@ descripcion: validaciones para el formulario de registro y envío de datos al backend mediante fetch.
*/

async function validacionCampos(event) {
    event.preventDefault(); // Evitamos que el formulario recargue la página de forma tradicional

    // Captura de valores limpios de espacios en blanco
    const nombre = document.getElementById("nombre").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmacion = document.getElementById("confirm-password").value;
    const terminos = document.getElementById("terms").checked; // Usamos .checked para checkboxes

    if (nombre === "" || email === "" || password === "" || confirmacion === "") {
        alert("Por favor, completa todos los campos obligatorios.");
        return false;
    }

    if (password !== confirmacion) {
        alert("Las contraseñas no coinciden. Revisa e intentalo de nuevo.");
        return false;
    }

    if (!terminos) {
        alert("Debes aceptar el tratamiento de datos personales (Ley 1581) para continuar.");
        return false;
    }

    // enviamos los datos al backend de FastAPI
    const datosUsuario = {
        nombre: nombre,
        correo: email,
        contrasena: password
    };

    try {
        const respuesta = await fetch('/auth/registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosUsuario)
        });

        const data = await respuesta.json();

        if (respuesta.ok) {
            alert("Registro exitoso");
            window.location.href = '/login'; // Redirige al login tras registrarse con éxito
        } else {
            alert(data.detail || 'Ocurrió un error al registrar el usuario.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('No se pudo conectar con el servidor.');
    }

    return false;
}



/*
@ Autor: Jhon Esteban Garcia Florez
@ fecha: 11/09/2026
@ descripcion: Crear un icono para de ojo para mostrar la contrasena o ocultarla.
*/

document.addEventListener('DOMContentLoaded', () => {
    const toggleButtons = document.querySelectorAll('.btn-toggle-password');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
        const targetId = button.getAttribute('data-target');
        const input = document.getElementById(targetId);

        if (input.type === 'password') {
            // Mostrar contraseña
            input.type = 'text';
            button.innerHTML = '<i data-lucide="eye-off"></i>';
            button.setAttribute('aria-label', 'Ocultar contraseña');
        } else {
            // Ocultar contraseña
            input.type = 'password';
            button.innerHTML = '<i data-lucide="eye"></i>';
            button.setAttribute('aria-label', 'Mostrar contraseña');
        }

        lucide.createIcons();
        });
    });
});


