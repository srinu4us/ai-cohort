# Structured SQL Queries Reference

## 1. Deductible for Gold PPO

**Question:** What's the deductible on the Gold PPO plan?

**SQL:**
```sql
SELECT annual_deductible
FROM plans
WHERE plan_name = 'Gold PPO';
```

**Output:**
```text
(2000,)
```

## 2. Pending claims for member M1001

**Question:** How many claims are pending for member M1001?

**SQL:**
```sql
SELECT COUNT(*)
FROM claims
WHERE member_id = 'M1001' AND status = 'Pending';
```

**Output:**
```text
(1,)
```

## 3. Plans with monthly premium under $400

**Question:** Which plans have a monthly premium under $400?

**SQL:**
```sql
SELECT plan_id, plan_name, monthly_premium
FROM plans
WHERE monthly_premium < 400
ORDER BY monthly_premium;
```

**Output:**
```text
('P103', 'Bronze HMO', 150)
('P102', 'Silver HMO', 300)
```

## 4. Join between claims and plans

**Question:** Show claims with their associated plan information.

**SQL:**
```sql
SELECT c.claim_id, c.member_id, p.plan_name, c.status, c.claim_amount
FROM claims c
JOIN plans p ON c.plan_id = p.plan_id
ORDER BY c.claim_id;
```

**Output:**
```text
('C1001', 'M1001', 'Gold PPO', 'Pending', 250)
('C1002', 'M1001', 'Gold PPO', 'Approved', 1200)
('C1003', 'M1002', 'Silver HMO', 'Denied', 150)
('C1004', 'M1002', 'Silver HMO', 'Approved', 900)
('C1005', 'M1003', 'Bronze HMO', 'Pending', 50)
```

## 5. Top-N query for most claimed procedures

**Question:** What are the most commonly claimed procedures?

**SQL:**
```sql
SELECT procedure, COUNT(*) AS claim_count
FROM claims
GROUP BY procedure
ORDER BY claim_count DESC, procedure
LIMIT 3;
```

**Output:**
```text
('X-ray', 3)
('Surgery', 2)
```
