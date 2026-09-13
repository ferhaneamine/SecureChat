# SecureChat 🔐

A real-time secure messaging application developed as a mini-project in Computer Science (Data Science).

## Overview

SecureChat is a client-server messaging application designed to demonstrate core cybersecurity and cryptography concepts. Messages are encrypted on the client side before being transmitted through the server.

## Security

The application uses:

- **AES-256-GCM** — encrypts the message content.
- **RSA-OAEP 2048-bit** — encrypts the randomly generated AES key for the recipient.
- **SHA-256** — verifies message integrity.
- **Web Crypto API** — performs cryptographic operations locally in the browser.
- **WebSockets / Flask-SocketIO** — provides real-time communication.

The server receives and forwards the encrypted payload rather than the plaintext message.

## How it works

1. A user connects with a username.
2. An RSA public/private key pair is generated locally.
3. Public keys are exchanged between connected users.
4. When sending a message:
   - A random AES-256 key is generated.
   - The message is encrypted with AES-256-GCM.
   - The AES key is encrypted with the recipient's RSA public key.
   - A SHA-256 hash is calculated for integrity verification.
5. The encrypted payload is sent through the Flask-SocketIO server.
6. The recipient decrypts the AES key with their RSA private key, decrypts the message, and verifies its hash.

## Features

- Real-time messaging
- Multiple connected users
- Local RSA key generation
- AES-256-GCM message encryption
- RSA-OAEP key protection
- SHA-256 integrity verification
- Encryption status indicator
- Encrypted payload / crypto inspector
- Unread message notifications
- Simple modern dark interface

## Project Structure

```text
SecureChat/
├── server.py
├── templates/
│   └── index.html
├── static/
├── screenshots/
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd SecureChat
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python server.py
```

Then open:

```text
http://127.0.0.1:5000
```

To test multiple users, open the application in multiple browser tabs and connect with a different username in each tab.


## Limitations

The current project is a prototype and has known limitations:

- No secure user authentication
- RSA keys are not persisted and are lost after disconnection
- No digital signatures
- No protection against replay or spoofing attacks
- Messages are not persisted

## Future Improvements

- Add secure user authentication
- Implement digital signatures
- Persist encrypted messages
- Add group conversations
- Improve key management

## Technologies

Python · Flask · Flask-SocketIO · HTML · CSS · JavaScript · Web Crypto API
