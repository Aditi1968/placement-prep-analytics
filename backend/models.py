from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    company = Column(String(120), index=True)
    role = Column(String(120), index=True)
    difficulty = Column(String(20), index=True)  # Easy/Medium/Hard
    text = Column(Text)
    solution_link = Column(String(500), nullable=True)
    tags = Column(String(250), nullable=True)

class Learner(Base):
    __tablename__ = "learners"
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    email = Column(String(200), unique=True)
    batch = Column(String(50), index=True)

class Test(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    company = Column(String(120), index=True)
    role = Column(String(120), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    questions = relationship("TestQuestion", back_populates="test", cascade="all, delete-orphan")

class TestQuestion(Base):
    __tablename__ = "test_questions"
    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    ord = Column(Integer, default=0)
    test = relationship("Test", back_populates="questions")
    question = relationship("Question")

class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True)
    learner_id = Column(Integer, ForeignKey("learners.id", ondelete="SET NULL"))
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    correct = Column(Boolean, default=False)
    time_taken_s = Column(Integer, default=0)
    fail_reason = Column(String(250), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Survey(Base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True)
    learner_id = Column(Integer, ForeignKey("learners.id", ondelete="SET NULL"), nullable=True)
    company = Column(String(120))
    role = Column(String(120))
    feedback = Column(Text)
    sentiment = Column(String(20))
    theme = Column(String(120))
    created_at = Column(DateTime, default=datetime.utcnow)

class Bootcamp(Base):
    __tablename__ = "bootcamps"
    id = Column(Integer, primary_key=True)
    topic = Column(String(200))
    company = Column(String(120))
    role = Column(String(120))
    starts_at = Column(DateTime)
    mode = Column(String(20), default="online")
    capacity = Column(Integer, default=100)
    location = Column(String(200), nullable=True)
