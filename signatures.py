from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA


class Verifier:
    algorithm = ECDSA(hashes.SHA256())

    def __init__(self, public_key: bytes):
        # if type(public_key) is str:  # public_key comes as hex string
        #     public_key = bytes.fromhex(public_key)
        self.key = serialization.load_der_public_key(public_key, backend=default_backend())

    def verify(self, message: bytes, signature: bytes) -> bool:
        try:
            self.key.verify(signature, message, self.algorithm)
            return True
        except InvalidSignature:
            return False
