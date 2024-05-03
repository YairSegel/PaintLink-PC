from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA

# Assume public_key_hex contains the hex-encoded public key
public_key_hex = "3059301306072a8648ce3d020106082a8648ce3d03010703420004a4b4eb30a90388233e7c14a7e3c3ec2f53badc00c6d756fb5976a83a79808b239f3c9ae06ab01d760ccd7630d1f93df3a645dc94d732a00d2e308823a2b614c4"
pubkey_bytes = bytes.fromhex(public_key_hex)

public_key = serialization.load_der_public_key(pubkey_bytes, backend=default_backend())

# Assume signature_hex contains the hex-encoded signature
signature_hex = "304502207cd02df3ab8d172bf0fc77f2af55fc7882969158ec2249d1449684ef816bcab6022100d6ae90bbeb0e049ee38cef5e51769b9be635df9b1ce25ca8a4714c78382ee4fd"
signature_bytes = bytes.fromhex(signature_hex)

# Assume message contains the message that was signed
message = b"Hello, Python server!"

# Verify the signature
try:
    public_key.verify(
        signature_bytes,
        message,
        ECDSA(hashes.SHA256())
    )
    print("Signature is valid.")
    public_key.verify(
        signature_bytes,
        message,
        ECDSA(hashes.SHA256())
    )
    print("Signature is valid.")
except InvalidSignature:
    print("Signature is invalid.")
