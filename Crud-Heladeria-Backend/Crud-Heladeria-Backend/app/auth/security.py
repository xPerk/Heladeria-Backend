from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from typing import Optional
import secrets
import base64

# Configurar el contexto de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash de una contraseña usando bcrypt
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar si una contraseña coincide con su hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str) -> Optional[Usuario]:
    """
    Autenticar un usuario con username y password
    """
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user

def decode_basic_auth(authorization: str) -> tuple[str, str] | None:
    """
    Decodificar las credenciales de HTTP Basic Auth
    """
    try:
        # Remover 'Basic ' del inicio
        if not authorization.startswith('Basic '):
            return None
        
        encoded_credentials = authorization[6:]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        
        # Separar username y password
        if ':' not in decoded_credentials:
            return None
            
        username, password = decoded_credentials.split(':', 1)
        return username, password
    except Exception:
        return None