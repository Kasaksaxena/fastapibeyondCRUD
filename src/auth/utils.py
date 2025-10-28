from passlib.context import CryptContext

# Create the context, specifying bcrypt as the algorithm.
# Deprecated="auto" tells passlib to handle future algorithm upgrades if needed.
pass_context=CryptContext(schemes=["bycript"],depricated="auto")

def generate_pass_hash(plain_pass:str) -> str:
    """Takes a plain password and returns its bcrypt hash."""
    return pass_context.hash(plain_pass)

def verify_pass(plain_pass: str, hash_pass : str) -> bool:
    
    return pass_context.verify(plain_pass,hash_pass)