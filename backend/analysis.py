import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text
from .database import engine
from .config import CHART_DIR

def kpis():
    with engine.connect() as con:
        qn = con.execute(text("select count(*) from questions")).scalar() or 0
        tn = con.execute(text("select count(*) from tests")).scalar() or 0
        an = con.execute(text("select count(*) from attempts")).scalar() or 0
        ln = con.execute(text("select count(*) from learners")).scalar() or 0
    return dict(questions=qn, tests=tn, attempts=an, learners=ln)

def success_by_company_role():
    sql = """
    select q.company, q.role,
           avg(case when a.correct then 1.0 else 0.0 end) as success_rate,
           count(*) as n_attempts
    from attempts a
    join questions q on q.id = a.question_id
    group by q.company, q.role
    having count(*) >= 1
    order by success_rate desc
    """
    df = pd.read_sql(text(sql), engine)
    if not df.empty:
        path = os.path.join(CHART_DIR, "success_by_company_role.png")
        plt.figure()
        df.plot(kind="bar", x="company", y="success_rate", title="Success Rate by Company (avg across roles)")
        plt.tight_layout(); plt.savefig(path); plt.close()
        return path, df
    return None, df

def top_gaps(limit=10):
    sql = """
    select fail_reason, count(*) as n
    from attempts
    where fail_reason is not null and fail_reason <> ''
    group by fail_reason
    order by n desc
    limit :lim
    """
    df = pd.read_sql(text(sql), engine, params={"lim": limit})
    if not df.empty:
        path = os.path.join(CHART_DIR, "top_gaps.png")
        plt.figure()
        df.plot(kind="bar", x="fail_reason", y="n", title="Top Failure Reasons")
        plt.tight_layout(); plt.savefig(path); plt.close()
        return path, df
    return None, df
