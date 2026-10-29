from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db.database import Base, engine
from app.api.auth import router as auth_router
from fastapi import Request
from fastapi.responses import HTMLResponse

# 1. Crear automáticamente las tablas en MySQL si aún no existen
Base.metadata.create_all(bind=engine)

# 2. Inicializar la aplicación FastAPI
app = FastAPI(
    title="A.L.I.C.I.A API",
    description="Asistente Local con Inteligencia Cognitiva e Interacción Académica",
    version="1.0.0"
)

# 3. Montar la carpeta de archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 4. Configurar el motor de plantillas HTML
templates = Jinja2Templates(directory="templates")

# 5. Registrar los routers de la API
app.include_router(auth_router)


# --- RUTAS DE NAVEGACIÓN FRONTEND ---
@app.get("/")
def render_index(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.get("/login")
def render_login(request: Request):
    return templates.TemplateResponse(request, "inicioSesion.html", {})

@app.get("/registro")
def render_registro(request: Request):
    return templates.TemplateResponse(request, "registrarse.html", {})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", {})

@app.get("/recuperar", response_class=HTMLResponse)
def vista_recuperar(request: Request):
    return templates.TemplateResponse(request ,"recuperarContrasena.html", {})

@app.get("/restablecer", response_class=HTMLResponse)
def vista_restablecer(request: Request):
    return templates.TemplateResponse(request,"restablecerContrasena.html", {})





