from datetime import datetime, timedelta
from jose import JWTError, jwt

secret_key = "secret"
algorithm = "HS256"
access_expiry_time = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = access_expiry_time)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, secret_key, algorithm = algorithm)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms = [algorithm])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None