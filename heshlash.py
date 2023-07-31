import hashlib
import re

def hash_password(password:str):
    sha256  = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()
    return hashed_password
