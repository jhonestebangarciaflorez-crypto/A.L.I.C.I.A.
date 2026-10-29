from pydantic import BaseModel, EmailStr

class PasswordResetRequest(BaseModel):
    correo: EmailStr

class PasswordResetConfirm(BaseModel):
    token_o_codigo: str
    nueva_contrasena: str




    