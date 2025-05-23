# Python Project

This is a Python project template with a basic structure for development.

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

- Windows:

```bash
.\venv\Scripts\activate
```

- Unix/MacOS:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Project Structure

- `src/`: Contains the main source code
- `tests/`: Contains unit tests
- `requirements.txt`: Lists project dependencies

## Development

- Run tests: `pytest`
- Format code: `black src tests`
- Lint code: `flake8 src tests`
