from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.usuario import Usuario
from app.auth.security import authenticate_user

# Configurar HTTP Basic Auth
security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)) -> Usuario:
    """
    Dependencia para obtener el usuario actual autenticado
    """
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

def get_current_active_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """
    Dependencia para obtener el usuario actual activo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user