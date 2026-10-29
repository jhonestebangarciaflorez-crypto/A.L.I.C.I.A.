from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class RecuperacionContrasena(Base):
    __tablename__ = "recuperacion_contrasena"

    id_recuperacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    correo = Column(String(150), nullable=False)
    contrasena = Column(String(255), nullable=True)
    token_recuperacion = Column(String(255), nullable=True)
    codigo_verificacion = Column(String(50), nullable=True)
    fecha_expiracion = Column(DateTime, nullable=True)
    nueva_contrasena = Column(String(255), nullable=True)
    ultima_contrasena = Column(String(255), nullable=True)

    # Relación inversa opcional con el modelo Usuario (si la necesitas)
    usuario = relationship("Usuario")






    