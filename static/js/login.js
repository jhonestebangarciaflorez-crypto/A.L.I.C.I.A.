/* 
@ Autor: Jhon Esteban Garcia Florez
@ Descripcion: Inicialización segura de Lucide y lógica de autenticación para el login.
*/

// 1. Inicializar los iconos de Lucide cuando el DOM cargue por completo
document.addEventListener('DOMContentLoaded', () => {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

// 2. Función independiente para manejar el envío del formulario de login
async function iniciarSesion(event) {
    event.preventDefault(); // Evita el recargo de la página

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (email === "" || password === "") {
        alert("Por favor, completa todos los campos.");
        return false;
    }

    const credenciales = {
        correo: email,
        contrasena: password
    };

    try {
        const respuesta = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credenciales)
        });

        const data = await respuesta.json();

        if (respuesta.ok) {
            alert("¡Inicio de sesión exitoso! Bienvenido de nuevo.");
            window.location.href = '/dashboard'; // Redirige al inicio o al dashboard
        } else {
            alert(data.detail || 'Correo o contraseña incorrectos.');
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        alert('No se pudo conectar con el servidor.');
    }

    return false;
};









