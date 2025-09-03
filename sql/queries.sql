-- Success rate by company/role
SELECT q.company, q.role,
       AVG(CASE WHEN a.correct THEN 1.0 ELSE 0.0 END) AS success_rate,
       COUNT(*) AS n_attempts
FROM attempts a
JOIN questions q ON q.id = a.question_id
GROUP BY q.company, q.role
ORDER BY success_rate DESC;
