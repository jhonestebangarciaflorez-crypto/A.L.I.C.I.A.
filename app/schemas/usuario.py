from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

# 1. Esquema base con atributos comunes
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del usuario")
    apellidos: Optional[str] = Field(None, max_length=100)
    correo: EmailStr = Field(..., description="Correo electrónico válido")

# 2. Esquema para la entrada del formulario de registro (recibe la contraseña en texto plano)
class UsuarioCrear(UsuarioBase):
    contrasena: str = Field(..., min_length=6, description="Contraseña de al menos 6 caracteres")
    fecha_nacimiento: Optional[date] = None
    id_rol: int = Field(4, description="Por defecto 4 (Usuario)")

# 3. Esquema para la entrada del formulario de Inicio de Sesión
class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str

# 4. Esquema de respuesta para el cliente (Lo que la API devuelve al Frontend)
class UsuarioRespuesta(UsuarioBase):
    id_usuario: int
    id_rol: int
    estado_cuenta: str

    class Config:
        from_attributes = True  # Permite que Pydantic lea directamente objetos de SQLAlchemy



