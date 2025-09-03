import pandas as pd
from .database import SessionLocal
from .models import Survey

POS_WORDS = set("good great helpful clear confident improved fast".split())
NEG_WORDS = set("bad confusing slow hard tough unclear anxious".split())

def quick_sentiment(text:str)->str:
    t = text.lower()
    pos = sum(w in t for w in POS_WORDS)
    neg = sum(w in t for w in NEG_WORDS)
    if pos>neg: return "Positive"
    if neg>pos: return "Negative"
    return "Neutral"

def theme_from_text(text:str)->str:
    t = text.lower()
    if "sql" in t: return "SQL"
    if "dp" in t or "dynamic" in t: return "DP"
    if "graph" in t: return "Graphs"
    if "array" in t or "two pointers" in t: return "DSA Speed"
    if "behavioral" in t or "hr" in t: return "Behavioral"
    return "General"

def import_csv(path:str):
    df = pd.read_csv(path)
    sess = SessionLocal()
    try:
        for _, r in df.iterrows():
            fb = str(r.get("feedback",""))
            sess.add(Survey(
                learner_id=r.get("learner_id"),
                company=str(r.get("company","")),
                role=str(r.get("role","")),
                feedback=fb,
                sentiment=quick_sentiment(fb),
                theme=theme_from_text(fb)
            ))
        sess.commit()
    finally:
        sess.close()
