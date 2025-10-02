# TextArmor
# A tool that encodes and decodes text with password.
# Author - WireBits

import os
import sys
import base64
import getpass

def show_banner():
    print("+─────────────────────────────────+")
    print("|  ╔╦╗╔═╗═╗ ╦╔╦╗╔═╗╦═╗╔╦╗╔═╗╦═╗   |")
    print("|   ║ ║╣ ╔╩╦╝ ║ ╠═╣╠╦╝║║║║ ║╠╦╝   |")
    print("|   ╩ ╚═╝╩ ╚═ ╩ ╩ ╩╩╚═╩ ╩╚═╝╩╚═   |")
    print("+─────────────────────────────────+")
    print("| Text Encryption/Decryption Tool |")
    print("+─────────────────────────────────+")
    print("|        Author : WireBits        |")
    print("+─────────────────────────────────+")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def process():
    clear_screen()
    show_banner()
    print("+──────+")
    print("| Mode |")
    print("+──────+")
    print("╰┈➤ Base64      : b64")
    print("╰┈➤ Hexadecimal : hex")
    print("╰┈➤ Binary      : bin")
    print("╰┈➤ Octal       : oct")
    mode = get_input("╰┈➤ Select Mode ⮞ ", ['b64', 'hex', 'bin', 'oct'])
    
    print("+─────────────────+")
    print("| Encryption Type |")
    print("+─────────────────+")
    print("╰┈➤ Encode : e")
    print("╰┈➤ Decode : d")
    action = get_input("╰┈➤ Select Encryption Type ⮞ ", ['e', 'd'])
    message = get_message_input()
    if message is None:
        return

    key = getpass.getpass("╰┈➤ Enter password (supports special characters) ⮞ ").strip()
    if not key:
        print("╰┈➤ [!] Password cannot be empty!")
        return

    backup_choice = input("╰┈➤ Do you want to backup password? (yes/no) ⮞ ").strip().lower()
    if backup_choice in ['yes', 'y']:
        try:
            with open("password_backup.txt", "w", encoding="utf-8") as f:
                f.write(key)
            print("╰┈➤ Password backed up to password_backup.txt")
        except Exception as e:
            print(f"╰┈➤ Error saving password backup: {e}")

    try:
        if mode == 'b64':
            result = encode_base64(key, message) if action == 'e' else decode_base64(key, message)
        elif mode == 'hex':
            result = encode_hex(key, message) if action == 'e' else decode_hex(key, message)
        elif mode == 'bin':
            result = encode_binary(key, message) if action == 'e' else decode_binary(key, message)
        elif mode == 'oct':
            result = encode_octal(key, message) if action == 'e' else decode_octal(key, message)
        else:
            raise ValueError("Invalid mode.")

        handle_output(result)
    except Exception as e:
        print(f"\nError: {e}")

def get_message_input():
    print("+──────────+")
    print("|   Data   |")
    print("+──────────+")
    print("╰┈➤ String    : s")
    print("╰┈➤ .txt file : f")
    data_type = get_input("╰┈➤ Select Data ⮞ ", ['s', 'f'])
    if data_type == 's':
        return input("╰┈➤ Enter the text ⮞ ")
    else:
        while True:
            file_path = input("╰┈➤ Enter path to the .txt file ⮞ ").strip()
            if not os.path.isfile(file_path):
                print("╰┈➤ [!] File not found. Please try again!\n")
                continue
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

def handle_output(result):
    print("+───────────+")
    print("| View Mode |")
    print("+───────────+")
    print("╰┈➤ .txt file     : t")
    print("╰┈➤ Direct Output : show")
    while True:
        view_choice = input("╰┈➤ Select View ⮞ ").strip().lower()
        if view_choice == 't':
            filename = input("╰┈➤ Enter file name (without extension) ⮞ ").strip()
            if not filename.endswith(".txt"):
                filename += ".txt"
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"╰┈➤ Output saved to: {filename}")
            except Exception as e:
                print(f"Error saving file: {e}")
            break
        elif view_choice == 'show':
            print("╰┈➤ Final Output : \n")
            print(result)
            break
        else:
            print("╰┈➤ [!] Invalid input! Please try again!\n")

def encode_base64(key, message):
    enc = [chr((ord(message[i]) + ord(key[i % len(key)])) % 256) for i in range(len(message))]
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode_base64(key, message):
    try:
        decoded = base64.urlsafe_b64decode(message).decode()
    except Exception:
        raise ValueError("Invalid Base64 input.")
    return ''.join([chr((256 + ord(decoded[i]) - ord(key[i % len(key)])) % 256) for i in range(len(decoded))])

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

def encode_binary(key, message):
    return ' '.join([bin((ord(message[i]) + ord(key[i % len(key)])) % 256)[2:].zfill(8) for i in range(len(message))])

def decode_binary(key, message):
    bits = message.split()
    dec = []
    for i, b in enumerate(bits):
        try:
            val = int(b, 2)
        except Exception:
            raise ValueError("Invalid Binary input.")
        key_c = key[i % len(key)]
        dec.append(chr((256 + val - ord(key_c)) % 256))
    return ''.join(dec)

def encode_octal(key, message):
    return ' '.join([oct((ord(message[i]) + ord(key[i % len(key)])) % 256)[2:].zfill(3) for i in range(len(message))])

def decode_octal(key, message):
    parts = message.split()
    dec = []
    for i, p in enumerate(parts):
        try:
            val = int(p, 8)
        except Exception:
            raise ValueError("Invalid Octal input.")
        key_c = key[i % len(key)]
        dec.append(chr((256 + val - ord(key_c)) % 256))
    return ''.join(dec)

def get_input(prompt, valid_values):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_values:
            return user_input
        print("╰┈➤ [!] Invalid input! Please try again!\n")

try:
    import readline
except ImportError:
    try:
        import pyreadline as readline
    except ImportError:
        try:
            import pyreadline3 as readline
        except ImportError:
            readline = None

if readline:
    import glob
    def complete_path(text, state):
        line = readline.get_line_buffer().split()
        if not line:
            return [None][state]
        else:
            return (glob.glob(os.path.expanduser(text) + '*') + [None])[state]

    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete_path)

def main():
    while True:
        process()
        cont = input("\n╰┈➤ Do you want to continue? (yes/no) ⮞ ").strip().lower()
        if cont not in ['yes', 'y']:
            print("\n╰┈➤ [!] Exiting the tool. Goodbye!")
            break

if __name__ == "__main__":
    try:
        os.system('clear')
        main()
    except KeyboardInterrupt:
        print('\n╰┈➤ [!] Closing the tool. Goodbye!')
        exit(0)
    except Exception as e:
        print('╰┈➤[!] ERROR: ' + str(e))