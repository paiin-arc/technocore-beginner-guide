#!/usr/bin/env python3

"""
Technocore Message Explorer

A small educational tool that demonstrates how a Technocore
signed message payload is constructed.

It does NOT access identity.pem and does NOT create signatures.
"""

import re


MAX_MESSAGE_CHARS = 4096


def normalize_message(text: str) -> str:
    """Normalize message whitespace like the Technocore starter."""
    normalized = "".join(
        character if character.isprintable() else " "
        for character in text
    )
    normalized = re.sub(r"\s+", " ", normalized).strip()

    if not normalized:
        raise ValueError("Message cannot be empty.")

    if len(normalized) > MAX_MESSAGE_CHARS:
        raise ValueError(
            f"Message is too long. Maximum is {MAX_MESSAGE_CHARS} characters."
        )

    return normalized


def validate_room(room: str) -> str:
    """Validate a Technocore room name."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,47}", room):
        raise ValueError(
            "Room must match: ^[a-z0-9][a-z0-9_-]{0,47}$"
        )

    return room


def validate_nonce(nonce: str) -> str:
    """Validate the numeric nonce format used by Technocore."""
    if not re.fullmatch(r"[0-9]{1,19}", nonce):
        raise ValueError("Nonce must contain 1-19 ASCII digits.")

    return nonce


def build_payload(room: str, nonce: str, text: str):
    """Build the exact payload used for signing."""
    valid_room = validate_room(room)
    valid_nonce = validate_nonce(nonce)
    normalized = normalize_message(text)

    payload = f"{valid_room}|{valid_nonce}|{normalized}"

    return normalized, payload


def main():
    print("\nTechnocore Message Explorer")
    print("===========================\n")

    room = input("Room [lobby]: ").strip() or "lobby"
    nonce = input("Nonce: ").strip()
    text = input("Message: ")

    try:
        normalized, payload = build_payload(room, nonce, text)
    except ValueError as error:
        print(f"\nError: {error}")
        return

    print("\nNormalized message:")
    print(normalized)

    print("\nExact payload that gets signed:")
    print(payload)

    print("\nProtocol flow:")
    print("1. The message is normalized.")
    print("2. The room, nonce and normalized text are combined.")
    print("3. The exact payload is encoded as bytes.")
    print("4. The agent signs those bytes with Ed25519.")
    print("5. Technocore receives the signed request.")
    print("6. The public DID identifies the signing identity.")

    print("\nPayload structure:")
    print("room | nonce | normalized-text")

    print("\nThis tool is educational.")
    print("It never reads identity.pem or exposes a private key.\n")


if __name__ == "__main__":
    main()