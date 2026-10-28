"""Entry point for Vercel and uvicorn (`uvicorn index:app`).

Vercel loads this file directly, so it must sit at the project root and use an
absolute import; loading app/web.py on its own would break its relative imports.
"""

from app.web import app  # noqa: F401
