#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════╗
║         K E Y 3 I Y A L   v2.0                   ║
║         Secret Message Encryptor                  ║
║         Original algorithm by 3IYAL              ║
╚═══════════════════════════════════════════════════╝
"""

import os
import sys
from random import randint

# ── ANSI color codes ──────────────────────────────
R  = "\033[0m"        # reset
B  = "\033[1m"        # bold
G  = "\033[92m"       # bright green
Y  = "\033[93m"       # bright yellow
C  = "\033[96m"       # bright cyan
M  = "\033[95m"       # magenta
RE = "\033[91m"       # red
DM = "\033[2m"        # dim


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(f"""
{G}{B}  ██╗  ██╗███████╗██╗   ██╗██████╗ ██╗██╗   ██╗ █████╗ ██╗{R}
{G}{B}  ██║ ██╔╝██╔════╝╚██╗ ██╔╝╚════██╗██║╚██╗ ██╔╝██╔══██╗██║{R}
{G}{B}  █████╔╝ █████╗   ╚████╔╝  █████╔╝██║ ╚████╔╝ ███████║██║{R}
{G}{B}  ██╔═██╗ ██╔══╝    ╚██╔╝   ╚═══██╗██║  ╚██╔╝  ██╔══██║██║{R}
{G}{B}  ██║  ██╗███████╗   ██║   ██████╔╝██║   ██║   ██║  ██║███████╗{R}
{G}{B}  ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝{R}
{DM}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{R}
{C}           Secret Message Encryptor  •  v2.0{R}
{DM}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{R}
""")


def divider(char="─", color=DM):
    print(f"{color}  {'─' * 51}{R}")


def section(title):
    print(f"\n{C}{B}  ▸ {title}{R}")
    divider()


def success(msg):
    print(f"\n{G}  ✔  {msg}{R}")


def warn(msg):
    print(f"\n{Y}  ⚠  {msg}{R}")


def error(msg):
    print(f"\n{RE}  ✘  {msg}{R}")


def prompt(label):
    return input(f"\n{Y}  {label}{R}\n{DM}  >{R} ").strip()


# ── Core algorithm ────────────────────────────────
def encrypt(plaintext: str) -> tuple[str, str]:
    """
    For each character:
      - Generate a random offset in [0, 255 - ord(char)]
      - Add offset to char code
      - Store offset as part of the key
    Output is hex-encoded for clean, portable display.
    """
    enc_bytes = []
    key_bytes = []
    for ch in plaintext:
        code = ord(ch)
        if code > 255:
            raise ValueError(f"Character '{ch}' outside supported range (ASCII only).")
        offset = randint(0, 255 - code)
        enc_bytes.append(code + offset)
        key_bytes.append(offset)
    cipher = bytes(enc_bytes).hex().upper()
    key    = bytes(key_bytes).hex().upper()
    return cipher, key


def decrypt(cipher_hex: str, key_hex: str) -> str:
    """
    Reverses encrypt():
      - Parse hex strings back to byte arrays
      - Subtract key bytes from cipher bytes to recover originals
    """
    cipher_hex = cipher_hex.strip().upper()
    key_hex    = key_hex.strip().upper()

    if len(cipher_hex) != len(key_hex):
        raise ValueError("Cipher and key have different lengths — they must match.")
    if len(cipher_hex) % 2 != 0:
        raise ValueError("Cipher text length is odd — it looks corrupted.")
    if any(c not in "0123456789ABCDEF" for c in cipher_hex + key_hex):
        raise ValueError("Non-hex characters found. Did you copy the full cipher/key?")

    result = []
    for i in range(0, len(cipher_hex), 2):
        enc_byte = int(cipher_hex[i:i+2], 16)
        key_byte = int(key_hex[i:i+2], 16)
        original = enc_byte - key_byte
        if not (0 <= original <= 255):
            raise ValueError(f"Byte at position {i//2} is out of range — wrong key?")
        result.append(chr(original))
    return "".join(result)


# ── Encrypt flow ──────────────────────────────────
def run_encrypt():
    section("ENCRYPT MODE")
    print(f"{DM}  Your message will be locked with a one-time random key.{R}")

    message = prompt("Enter your message")
    if not message:
        error("Message cannot be empty.")
        return

    try:
        cipher, key = encrypt(message)
    except ValueError as e:
        error(str(e))
        return

    section("RESULT")
    print(f"\n{M}  {'ENCRYPTED CIPHER':20s}{R}")
    print(f"  {G}{cipher}{R}\n")

    print(f"{M}  {'YOUR SECRET KEY':20s}{R}")
    print(f"  {C}{key}{R}\n")

    divider(color=G)
    print(f"{DM}  ⚑  Share the CIPHER freely — it's unreadable without the key.")
    print(f"  ⚑  Keep the KEY secret. Without it, decryption is impossible.{R}")
    divider(color=G)

    print(f"\n{DM}  Stats  •  {len(message)} chars  •  {len(cipher)//2} bytes  •  key entropy: {len(key)//2 * 8} bits{R}")


# ── Decrypt flow ──────────────────────────────────
def run_decrypt():
    section("DECRYPT MODE")
    print(f"{DM}  Paste the cipher and its matching key to recover the message.{R}")

    cipher = prompt("Enter cipher text (hex)")
    if not cipher:
        error("Cipher text cannot be empty.")
        return

    key = prompt("Enter secret key (hex)")
    if not key:
        error("Key cannot be empty.")
        return

    try:
        plaintext = decrypt(cipher, key)
    except ValueError as e:
        error(str(e))
        return

    section("DECRYPTED MESSAGE")
    print(f"\n  {G}{B}{plaintext}{R}\n")
    divider(color=G)
    success("Message recovered successfully.")


# ── Main menu ─────────────────────────────────────
def main():
    clear()
    banner()

    print(f"  {B}What do you want to do?{R}\n")
    print(f"  {G}[1]{R}  Encrypt a message")
    print(f"  {C}[2]{R}  Decrypt a message")
    print(f"  {DM}[3]{R}  Exit\n")

    choice = prompt("Choose an option")

    if choice == "1":
        run_encrypt()
    elif choice == "2":
        run_decrypt()
    elif choice == "3":
        print(f"\n{DM}  Goodbye.{R}\n")
        sys.exit(0)
    else:
        error("Invalid option. Please choose 1, 2, or 3.")

    print()
    divider()
    again = prompt("Go again? [y/N]").lower()
    if again == "y":
        main()
    else:
        print(f"\n{DM}  Stay safe out there.{R}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{DM}  Interrupted. Goodbye.{R}\n")
        sys.exit(0)
