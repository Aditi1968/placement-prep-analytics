import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ppars.db")
CHART_DIR = os.path.join(os.path.dirname(__file__), "static", "charts")
os.makedirs(CHART_DIR, exist_ok=True)
