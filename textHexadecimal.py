def encode_hex(key, message):
    return ''.join([hex((ord(message[i]) + ord(key[i % len(key)])) % 256)[2:].zfill(2) for i in range(len(message))])

def decode_hex(key, message):
    if len(message) % 2 != 0:
        raise ValueError("Invalid Hex input.")
    dec = []
    for i in range(0, len(message), 2):
        hex_val = int(message[i:i+2], 16)
        key_c = key[(i // 2) % len(key)]
        dec.append(chr((256 + hex_val - ord(key_c)) % 256))
    return ''.join(dec)