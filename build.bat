@echo off
if not exist .venv (
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install pip-tools
    call .venv\Scripts\deactivate.bat
)

call .venv\Scripts\activate.bat
pip-compile requirements.in
pip-sync requirements.txt
python main.py
call .venv\Scripts\deactivate.bat