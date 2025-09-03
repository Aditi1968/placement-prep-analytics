from .database import Base, engine, SessionLocal
from .models import Question, Learner
import pandas as pd
from pathlib import Path

def main():
    Base.metadata.create_all(bind=engine)
    sess = SessionLocal()
    data_dir = Path(__file__).resolve().parents[1] / "data"
    qcsv = data_dir / "sample_questions.csv"
    lcsv = data_dir / "sample_learners.csv"

    if qcsv.exists():
        dfq = pd.read_csv(qcsv)
        for _, r in dfq.iterrows():
            sess.add(Question(
                company=r["company"], role=r["role"], difficulty=r["difficulty"],
                text=r["text"], solution_link=r.get("solution_link",""), tags=r.get("tags","")
            ))
    if lcsv.exists():
        dfl = pd.read_csv(lcsv)
        for _, r in dfl.iterrows():
            sess.add(Learner(name=r["name"], email=r["email"], batch=r["batch"]))
    sess.commit(); sess.close()
    print("Database initialized & seeded.")

if __name__ == "__main__":
    main()
