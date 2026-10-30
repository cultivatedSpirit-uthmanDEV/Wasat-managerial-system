import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DJANGO_DIR = BASE_DIR / "Django" / "Managerial"

sys.path.insert(0, str(DJANGO_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "Managerial.settings"
)

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()

