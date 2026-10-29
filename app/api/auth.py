from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCrear, UsuarioRespuesta, LoginRequest
from app.core.security import generar_hash_contrasena, verificar_contrasena
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.models.recuperacion import RecuperacionContrasena
from app.schemas.recuperacion import PasswordResetRequest, PasswordResetConfirm


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)



# 1. Endpoint para Registrar un Nuevo Usuario
@router.post("/registro", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario_data: UsuarioCrear, db: Session = Depends(get_db)):
    # Verificar si el correo ya está registrado en la BD
    usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario_data.correo).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado en el sistema."
        )

    # Hashear la contraseña antes de guardarla
    contrasena_encriptada = generar_hash_contrasena(usuario_data.contrasena)

    # Crear la instancia del modelo ORM
    nuevo_usuario = Usuario(
        nombre=usuario_data.nombre,
        apellidos=usuario_data.apellidos,
        correo=usuario_data.correo,
        contrasena=contrasena_encriptada,
        fecha_nacimiento=usuario_data.fecha_nacimiento,
        id_rol=usuario_data.id_rol
    )

    # Guardar en MySQL
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)  # Carga el id_usuario autogenerado

    return nuevo_usuario


# 2. Endpoint para Iniciar Sesión
@router.post("/login")
def iniciar_sesion(credenciales: LoginRequest, db: Session = Depends(get_db)):
    # Buscar el usuario por correo
    usuario = db.query(Usuario).filter(Usuario.correo == credenciales.correo).first()
    
    # Validar que el usuario exista y la contraseña coincida
    if not usuario or not verificar_contrasena(credenciales.contrasena, usuario.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos."
        )

    if usuario.estado_cuenta != "Activo":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta se encuentra inactiva."
        )

    return {
        "mensaje": "Inicio de sesión exitoso",
        "usuario": {
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "id_rol": usuario.id_rol
        }
    }


@router.post("/solicitar-recuperacion")
def solicitar_recuperacion(datos: PasswordResetRequest, db: Session = Depends(get_db)):
    # 1. Verificar si el correo existe en la tabla usuarios
    usuario = db.query(Usuario).filter(Usuario.correo == datos.correo).first()
    if not usuario:
        # Por seguridad, a veces se retorna un mensaje genérico
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El correo electrónico no se encuentra registrado en el sistema."
        )

    # 2. Generar un código de verificación de 6 dígitos y un token aleatorio
    codigo_verificacion = "".join([str(random.randint(0, 9)) for _ in range(6)])
    token_recuperacion = f"token-{usuario.id_usuario}-{random.randint(1000, 9999)}"
    
    # 3. Definir expiración
    fecha_expiracion = datetime.utcnow() + timedelta(minutes=5)

    # 4. Guardar o actualizar el registro en la tabla recuperacion_contrasena
    recuperacion_existente = db.query(RecuperacionContrasena).filter(RecuperacionContrasena.id_usuario == usuario.id_usuario).first()
    
    if recuperacion_existente:
        recuperacion_existente.token_recuperacion = token_recuperacion
        recuperacion_existente.codigo_verificacion = codigo_verificacion
        recuperacion_existente.fecha_expiracion = fecha_expiracion
        recuperacion_existente.correo = usuario.correo
    else:
        nueva_recuperacion = RecuperacionContrasena(
            id_usuario=usuario.id_usuario,
            correo=usuario.correo,
            token_recuperacion=token_recuperacion,
            codigo_verificacion=codigo_verificacion,
            fecha_expiracion=fecha_expiracion
        )
        db.add(nueva_recuperacion)

    db.commit()

    # Nota: Aquí conectarías tu lógica de envío de correos (SMTP / FastAPI-Mail).

    return {
        "mensaje": "Se ha enviado un código de verificación a su correo electrónico.",
        "correo": usuario.correo,
        "codigo_verificacion_mock": codigo_verificacion, # Únicamente para pruebas locales
        "token_recuperacion": token_recuperacion
    }

@router.post("/restablecer-contrasena")
def restablecer_contrasena(datos: PasswordResetConfirm, db: Session = Depends(get_db)):
    # 1. Buscar el registro de recuperación usando el código de verificación o el token
    recuperacion = db.query(RecuperacionContrasena).filter(
        (RecuperacionContrasena.token_recuperacion == datos.token_o_codigo) | 
        (RecuperacionContrasena.codigo_verificacion == datos.token_o_codigo)
    ).first()

    if not recuperacion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token o código de verificación es inválido."
        )

    # 2. Validar si el código ha expirado
    if recuperacion.fecha_expiracion and datetime.utcnow() > recuperacion.fecha_expiracion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El código de recuperación ha expirado. Solicite uno nuevo."
        )

    # 3. Buscar al usuario asociado
    usuario = db.query(Usuario).filter(Usuario.id_usuario == recuperacion.id_usuario).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )

    # 4. Actualizar la contraseña en la tabla usuarios (hasheada)
    usuario.contrasena = generar_hash_contrasena(datos.nueva_contrasena)
    
    # 5. Guardar contraseña anterior en el historial
    recuperacion.ultima_contrasena = usuario.contrasena
    recuperacion.nueva_contrasena = datos.nueva_contrasena

    # 6. Invalidar el token
    recuperacion.token_recuperacion = None
    recuperacion.codigo_verificacion = None
    recuperacion.fecha_expiracion = None

    db.commit()

    return {"mensaje": "Contraseña restablecida exitosamente."}