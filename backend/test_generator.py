from .database import SessionLocal
from .models import Test, TestQuestion, Question
import random

def generate_test(name:str, company:str, role:str, difficulty:str, n_questions:int=5):
    sess = SessionLocal()
    try:
        q = sess.query(Question).filter(
            Question.company.ilike(f"%{company}%"),
            Question.role.ilike(f"%{role}%"),
            Question.difficulty == difficulty
        ).all()
        if len(q) == 0:
            q = sess.query(Question).filter(
                Question.company.ilike(f"%{company}%"),
                Question.role.ilike(f"%{role}%")
            ).all()
        picked = random.sample(q, min(n_questions, len(q)))
        t = Test(name=name, company=company, role=role)
        sess.add(t); sess.flush()
        for i, qi in enumerate(picked):
            sess.add(TestQuestion(test_id=t.id, question_id=qi.id, ord=i+1))
        sess.commit()
        return t.id
    finally:
        sess.close()
