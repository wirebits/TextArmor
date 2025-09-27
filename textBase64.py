import base64

def encode_base64(key, message):
    enc = [chr((ord(message[i]) + ord(key[i % len(key)])) % 256) for i in range(len(message))]
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode_base64(key, message):
    try:
        decoded = base64.urlsafe_b64decode(message).decode()
    except Exception:
        raise ValueError("Invalid Base64 input.")
    return ''.join([chr((256 + ord(decoded[i]) - ord(key[i % len(key)])) % 256) for i in range(len(decoded))])