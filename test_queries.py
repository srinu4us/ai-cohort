import sqlite3
from pathlib import Path

conn = sqlite3.connect(Path(__file__).resolve().parent / 'coverage.db')
cur = conn.cursor()

queries = [
    ("Deductible for Gold PPO", "SELECT annual_deductible FROM plans WHERE plan_name = 'Gold PPO'"),
    ("Pending claims for M1001", "SELECT COUNT(*) FROM claims WHERE member_id = 'M1001' AND status = 'Pending'"),
    ("Plans under $400 premium", "SELECT plan_id, plan_name, monthly_premium FROM plans WHERE monthly_premium < 400 ORDER BY monthly_premium"),
    ("Join claims and plans", "SELECT c.claim_id, c.member_id, p.plan_name, c.status, c.claim_amount FROM claims c JOIN plans p ON c.plan_id = p.plan_id ORDER BY c.claim_id"),
    ("Top procedures", "SELECT procedure, COUNT(*) AS claim_count FROM claims GROUP BY procedure ORDER BY claim_count DESC, procedure LIMIT 3"),
]

for name, sql in queries:
    print(f'-- {name} --')
    print(sql)
    rows = cur.execute(sql).fetchall()
    for row in rows:
        print(row)
    print()

conn.close()
