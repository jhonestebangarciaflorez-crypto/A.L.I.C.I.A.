from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Rol(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre_rol = Column(String(50), nullable=False, unique=True)

    # Permite acceder a todos los usuarios de este rol: rol.usuarios
    usuarios = relationship("Usuario", back_populates="rol")


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=True)
    correo = Column(String(150), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    estado_cuenta = Column(Enum('Activo', 'Inactivo', name='estado_cuenta_enum'), nullable=False, default='Activo')
    fecha_desactivacion = Column(DateTime, nullable=True)
    id_admin = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)

    # Relaciones ORM para navegar entre objetos
    rol = relationship("Rol", back_populates="usuarios")
    admin = relationship("Usuario", remote_side=[id_usuario])





