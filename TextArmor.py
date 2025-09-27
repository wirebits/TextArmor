# TextArmor
# A tool that encodes and decodes text with password.
# Author - WireBits

import os
from textBase64 import encode_base64, decode_base64
from textHexadecimal import encode_hex, decode_hex

# ======================== Utility Functions ========================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    print(r"""
╔╦╗╔═╗═╗ ╦╔╦╗╔═╗╦═╗╔╦╗╔═╗╦═╗
 ║ ║╣ ╔╩╦╝ ║ ╠═╣╠╦╝║║║║ ║╠╦╝
 ╩ ╚═╝╩ ╚═ ╩ ╩ ╩╩╚═╩ ╩╚═╝╩╚═
    """)
    print("Developer: WireBits\n")

def get_input(prompt, valid_values):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_values:
            return user_input
        print("Invalid input. Please try again.\n")

def get_message_input():
    print("Data:")
    print("   s → String")
    print("   f → .txt file")
    data_type = get_input("Select Data : ", ['s', 'f'])
    if data_type == 's':
        return input("Enter the text: ")
    else:
        file_path = input("Enter path to the .txt file: ").strip()
        if not os.path.isfile(file_path):
            print("File not found.")
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

def handle_output(result):
    print("View Mode:")
    print("   t → .txt file")
    print("   show → Direct Output")
    view_choice = input("Select View : ").strip().lower()
    if view_choice == 't':
        filename = input("Enter file name (without extension): ").strip()
        if not filename.endswith(".txt"):
            filename += ".txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Output saved to: {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")
    elif view_choice == 'show':
        print("\nFinal Output:\n")
        print(result)
    else:
        print("Invalid view option. No output shown.")

# ======================== Core Logic ========================

def process():
    clear_screen()
    show_banner()

    print("Mode:")
    print("   b64 → Base64")
    print("   hex → Hexadecimal")
    mode = get_input("Select Mode : ", ['b64', 'hex'])

    print("Encryption Type:")
    print("   e → Encode")
    print("   d → Decode")
    action = get_input("Select Encryption Type : ", ['e', 'd'])

    message = get_message_input()
    if message is None:
        return

    key = input("Enter password (supports special characters): ").strip()
    if not key:
        print("Password cannot be empty.")
        return

    try:
        if mode == 'b64':
            result = encode_base64(key, message) if action == 'e' else decode_base64(key, message)
        else:
            result = encode_hex(key, message) if action == 'e' else decode_hex(key, message)

        handle_output(result)
    except Exception as e:
        print(f"\nError: {e}")

# ======================== Main Loop ========================

def main():
    while True:
        process()
        cont = input("\nDo you want to continue? (yes/no): ").strip().lower()
        if cont not in ['yes', 'y']:
            print("\nExiting the tool. Goodbye!")
            break

if __name__ == "__main__":
    main()