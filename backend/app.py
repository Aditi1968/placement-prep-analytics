from flask import Flask, render_template, request, redirect, url_for, send_file
from datetime import datetime
from io import BytesIO
from .database import SessionLocal, engine, Base
from .models import Question, Learner, Test, TestQuestion, Attempt, Bootcamp
from .analysis import kpis, success_by_company_role, top_gaps
from .test_generator import generate_test
from .survey_ingest import import_csv

app = Flask(__name__)

def init_db():
    Base.metadata.create_all(bind=engine)

# Initialize database once at startup (Flask 3 compatible)
with app.app_context():
    init_db()

    

@app.route('/')
def index():
    stats = kpis()
    s_path, _ = success_by_company_role()
    g_path, _ = top_gaps()
    return render_template('index.html',
                           stats=stats,
                           s_chart=s_path and ('/static/charts/' + s_path.split('/')[-1]),
                           g_chart=g_path and ('/static/charts/' + g_path.split('/')[-1]))

@app.route('/questions', methods=['GET','POST'])
def questions():
    sess = SessionLocal()
    try:
        if request.method == 'POST':
            q = Question(
                company=request.form.get('company','').strip(),
                role=request.form.get('role','').strip(),
                difficulty=request.form.get('difficulty','Easy'),
                text=request.form.get('text','').strip(),
                solution_link=request.form.get('solution_link','').strip(),
                tags=request.form.get('tags','').strip()
            )
            sess.add(q); sess.commit()
            return redirect(url_for('questions'))
        company = request.args.get('company','')
        role = request.args.get('role','')
        difficulty = request.args.get('difficulty','')
        qry = sess.query(Question)
        if company: qry = qry.filter(Question.company.ilike(f"%{company}%"))
        if role: qry = qry.filter(Question.role.ilike(f"%{role}%"))
        if difficulty: qry = qry.filter(Question.difficulty==difficulty)
        qs = qry.order_by(Question.company, Question.role, Question.difficulty).all()
        return render_template('questions.html', questions=qs)
    finally:
        sess.close()

@app.route('/tests', methods=['GET','POST'])
def tests():
    sess = SessionLocal()
    try:
        if request.method == 'POST':
            name = request.form.get('name','Last-Minute Prep')
            company = request.form.get('company','')
            role = request.form.get('role','')
            difficulty = request.form.get('difficulty','Medium')
            n = int(request.form.get('n','5'))
            tid = generate_test(name, company, role, difficulty, n)
            return redirect(url_for('test_detail', test_id=tid))
        ts = sess.query(Test).order_by(Test.created_at.desc()).all()
        return render_template('tests.html', tests=ts)
    finally:
        sess.close()

@app.route('/tests/<int:test_id>', methods=['GET','POST'])
def test_detail(test_id:int):
    sess = SessionLocal()
    try:
        t = sess.get(Test, test_id)
        tqs = sess.query(TestQuestion).filter_by(test_id=test_id).order_by(TestQuestion.ord).all()
        learners = sess.query(Learner).order_by(Learner.name).all()
        if request.method == 'POST':
            learner_id = int(request.form.get('learner_id'))
            for tq in tqs:
                c = request.form.get(f"correct_{tq.id}") == "on"
                reason = request.form.get(f"reason_{tq.id}") or ""
                sess.add(Attempt(learner_id=learner_id, test_id=test_id, question_id=tq.question_id,
                                 correct=c, fail_reason=reason.strip()))
            sess.commit()
            return redirect(url_for('test_detail', test_id=test_id))
        return render_template('test_detail.html', t=t, tqs=tqs, learners=learners)
    finally:
        sess.close()

@app.route('/learners', methods=['GET','POST'])
def learners():
    sess = SessionLocal()
    try:
        if request.method == 'POST':
            sess.add(Learner(name=request.form['name'], email=request.form['email'], batch=request.form['batch']))
            sess.commit()
            return redirect(url_for('learners'))
        ls = sess.query(Learner).order_by(Learner.batch, Learner.name).all()
        return render_template('learners.html', learners=ls)
    finally:
        sess.close()

@app.route('/attempts')
def attempts():
    sess = SessionLocal()
    try:
        rows = sess.query(Attempt).order_by(Attempt.created_at.desc()).limit(200).all()
        return render_template('attempts.html', attempts=rows)
    finally:
        sess.close()

@app.route('/analysis')
def analysis():
    s_path, _ = success_by_company_role()
    g_path, _ = top_gaps()
    return render_template('analysis.html',
                           s_chart=s_path and ('/static/charts/' + s_path.split('/')[-1]),
                           g_chart=g_path and ('/static/charts/' + g_path.split('/')[-1]))

@app.route('/surveys', methods=['GET','POST'])
def surveys():
    msg=None
    if request.method == 'POST':
        f = request.files.get('csv')
        if f:
            path = '/tmp/upload_surveys.csv'
            f.save(path)
            import_csv(path)
            msg = "Survey responses imported."
    return render_template('surveys.html', msg=msg)

def ics_for_bootcamp(topic, starts_at, location=""):
    dt = starts_at.strftime("%Y%m%dT%H%M%S")
    uid = f"{topic}-{dt}@ppars"
    ics = "BEGIN:VCALENDAR\n"
    ics += "VERSION:2.0\nPRODID:-//PPARS//EN\nBEGIN:VEVENT\n"
    ics += f"UID:{uid}\nDTSTAMP:{dt}Z\nDTSTART:{dt}Z\nDTEND:{dt}Z\n"
    ics += f"SUMMARY:{topic}\nLOCATION:{location}\nEND:VEVENT\nEND:VCALENDAR"
    return ics

@app.route('/bootcamps', methods=['GET','POST'])
def bootcamps():
    sess = SessionLocal()
    try:
        if request.method == 'POST':
            topic = request.form['topic']
            company = request.form.get('company','')
            role = request.form.get('role','')
            starts_at = datetime.fromisoformat(request.form['starts_at'])
            mode = request.form.get('mode','online')
            capacity = int(request.form.get('capacity','100'))
            location = request.form.get('location','')
            b = Bootcamp(topic=topic, company=company, role=role, starts_at=starts_at,
                         mode=mode, capacity=capacity, location=location)
            sess.add(b); sess.commit()
        bs = sess.query(Bootcamp).order_by(Bootcamp.starts_at.desc()).all()
        return render_template('bootcamps.html', bootcamps=bs)
    finally:
        sess.close()

@app.route('/bootcamps/<int:bid>/ics')
def bootcamp_ics(bid:int):
    sess = SessionLocal()
    try:
        b = sess.get(Bootcamp, bid)
        ics = ics_for_bootcamp(b.topic, b.starts_at, b.location or "")
        return send_file(BytesIO(ics.encode('utf-8')), as_attachment=True,
                         download_name=f"bootcamp_{bid}.ics", mimetype="text/calendar")
    finally:
        sess.close()
