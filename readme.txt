# Python TCP Chat Application

A multithreaded TCP chat server and client built in Python, with a full test suite covering unit and integration tests.

## Features

- Real-time messaging between multiple clients over TCP
- Nickname-based identity for each connected user
- Broadcast messages to all connected clients
- Graceful disconnect via `/exit` command
- Handles abrupt disconnections without crashing the server
- Input validation for messages (no empty messages, max 50 characters) and nicknames (no empty names, max 10 characters)
- Colorized server output using `colorama`

## Project Structure

```
Testing/
├── server.py                          # TCP server: handles connections, broadcasting, disconnects
├── client.py                          # TCP client: connects, sends and receives messages
├── validations.py                     # Input validation and message formatting utilities
├── unit_testing/
│   ├── test_validations.py            # Unit tests for message and nickname validation
│   └── test_server_functions.py       # Unit tests for broadcast and safe_send logic
├── integration_testing/
│   └── test_integration.py            # Integration tests for full client-server behaviour
└── .gitignore
```

## Requirements

- Python 3.x
- [colorama](https://pypi.org/project/colorama/)
- [pytest](https://pypi.org/project/pytest/) (for integration tests)

Install dependencies:

```bash
pip install colorama pytest
```

## Usage

### Start the Server

```bash
python server.py
```

The server listens on `127.0.0.1:9092` by default.

### Start a Client

```bash
python client.py
```

You will be prompted to enter a nickname (max 10 characters). Once connected, type messages and press Enter to send. Type `/exit` to leave the chat.

### Chat Rules

- Messages cannot be empty or whitespace-only
- Messages are limited to 50 characters
- Nicknames are limited to 10 characters

## Running Tests

### Unit Tests

```bash
cd unit_testing
python -m unittest discover
```

Covers:
- Empty and whitespace message rejection
- Message length limit (50 characters)
- Valid message acceptance
- Empty and whitespace nickname rejection
- Nickname length limit (10 characters)
- `broadcast()` calling `safe_send` for every connected client
- `safe_send()` retry logic on failure
- Client removal after exhausting retries

### Integration Tests

```bash
cd integration_testing
pytest test_integration.py
```

Covers:
- Single and multiple client connections
- Server correctly tracking nicknames
- Messages broadcast to all clients
- Multiple messages sent in sequence
- Client removal on `/exit`
- Other clients notified when someone leaves
- Abrupt disconnect handling
- Remaining clients unaffected by a dropped connection
