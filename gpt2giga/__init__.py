"""Force UTF-8 encoding for all text I/O.

On Windows the Python interpreter often defaults to ``cp1251`` / ``ascii``.
Importing this module first (before any other ``gpt2giga.*`` import) ensures
``PYTHONUTF8`` is active for child processes, and ``sys.stdout``/``sys.stderr``
are wrapped so loguru and other libraries always emit UTF-8 without
``UnicodeEncodeError`` when Russian or other non-ASCII text appears in
responses or error messages.
"""
import os
import sys

# For child processes spawned by uvicorn workers.
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# Wrap stdout/stderr so downstream code (loguru, print, etc.) always gets
# UTF-8 regardless of the Windows console codepage.
if sys.stdout.encoding != "utf-8":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", encoding="utf-8",
                           errors="replace", closefd=False, line_buffering=True)
if sys.stderr.encoding != "utf-8":
    sys.stderr = os.fdopen(sys.stderr.fileno(), "w", encoding="utf-8",
                           errors="replace", closefd=False, line_buffering=True)


from gpt2giga.api_server import run

__all__ = ["run"]

if __name__ == "__main__":
    run()
