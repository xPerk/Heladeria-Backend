from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin
from app.auth.security import hash_password, authenticate_user
from app.auth.dependencies import get_current_active_user

router = APIRouter(
    prefix="/auth",
    tags=["autenticación"]
)

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario
    """
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(Usuario).filter(Usuario.username == user.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está registrado"
            )
        
        # Crear nuevo usuario
        hashed_password = hash_password(user.password)
        db_user = Usuario(
            username=user.username,
            hashed_password=hashed_password,
            is_active=user.is_active
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el usuario. El nombre de usuario ya existe."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/login")
def login(user_credentials: UsuarioLogin, db: Session = Depends(get_db)):
    """
    Verificar credenciales de usuario (para testing)
    """
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return {
        "message": "Login exitoso",
        "user": {
            "id": user.id,
            "username": user.username,
            "is_active": user.is_active
        }
    }

@router.get("/me", response_model=UsuarioResponse)
def get_current_user_info(current_user: Usuario = Depends(get_current_active_user)):
    """
    Obtener información del usuario actual autenticado
    """
    return current_user

@router.get("/users", response_model=list[UsuarioResponse])
def get_all_users(current_user: Usuario = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Obtener todos los usuarios (requiere autenticación)
    """
    users = db.query(Usuario).all()
    return users