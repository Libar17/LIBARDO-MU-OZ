// === Listas vacías para guardar usuarios y contraseñ// === Función para mostrar formulario de registro ===
function mostrarRegistro() {
  document.getElementById('login').style.display = 'none';
  document.getElementById('registro').style.display = 'block';
}

// === Función para mostrar formulario de login ===
function mostrarLogin() {
  document.getElementById('registro').style.display = 'none';
  document.getElementById('login').style.display = 'block';
}

// === Función para mostrar pantalla en blanco con un mensaje ===
function pantallaEnBlanco(mensaje) {
  document.body.innerHTML = `<h1 style="text-align:center; margin-top:20%; font-family:sans-serif;">${mensaje}</h1>`;
  document.body.style.backgroundColor = "white";
}


// === Evento para el formulario de inicio de sesión ===
// Mandar inicio de sesion al backend
document.getElementById("formLogin").addEventListener("submit", async function(e) {
  e.preventDefault();

  const formData = new FormData(e.target);
  const mensajeLogin = document.getElementById("mensajeLogin");

  try {
    const res = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (res.ok && !data.error) {
      pantallaEnBlanco("✅ Iniciado sesión correctamente");
      mensajeLogin.textContent = "";
    } else {
      mensajeLogin.textContent = `❌ ${data.error || "Usuario o contraseña incorrectos"}`;
      mensajeLogin.style.color = "gray";
      mensajeLogin.style.fontStyle = "italic";
    }

    console.log(data);
  } catch (error) {
    mensajeLogin.textContent = "❌ Error de conexión con el servidor";
    mensajeLogin.style.color = "gray";
    mensajeLogin.style.fontStyle = "italic";
    console.error(error);
  }
});

// === Evento para el formulario de registro ===
// Mandar registro al backend
document.getElementById("formRegistro").addEventListener("submit", async function(e) {
  e.preventDefault();

  const formData = new FormData(e.target);
  const mensajeRegistro = document.getElementById("mensajeRegistro");

  try {
    const res = await fetch("http://127.0.0.1:8000/register", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (res.ok && !data.error) {
      pantallaEnBlanco("🎉 Cuenta creada exitosamente");
      mensajeRegistro.textContent = "";
    } else {
      mensajeRegistro.textContent = `❌ ${data.error || "Error al crear la cuenta"}`;
      mensajeRegistro.style.color = "gray";
      mensajeRegistro.style.fontStyle = "italic";
    }

    console.log(data);
  } catch (error) {
    mensajeRegistro.textContent = "❌ Error de conexión con el servidor";
    mensajeRegistro.style.color = "gray";
    mensajeRegistro.style.fontStyle = "italic";
    console.error(error);
  }
});


// === Eventos para cambiar entre formularios ===
document.getElementById("btnRegistro").addEventListener("click", mostrarRegistro);
document.getElementById("btnVolver").addEventListener("click", mostrarLogin);




