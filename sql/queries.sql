-- ==========================================
-- Query 1 : Top 5 Funds by AUM
-- ==========================================

SELECT
    f.scheme_name,
    a.aum_crore
FROM fact_aum a
JOIN dim_fund f
ON a.fund_id = f.fund_id
ORDER BY a.aum_crore DESC
LIMIT 5;

-- ==========================================
-- Query 2 : Top 5 Funds by 5-Year Return
-- ==========================================

SELECT
    f.scheme_name,
    p.return_5yr_pct
FROM fact_performance p
JOIN dim_fund f
ON p.fund_id = f.fund_id
ORDER BY p.return_5yr_pct DESC
LIMIT 5;

-- ==========================================
-- Query 3 : Highest Sharpe Ratio
-- ==========================================

SELECT
    f.scheme_name,
    p.sharpe_ratio
FROM fact_performance p
JOIN dim_fund f
ON p.fund_id = f.fund_id
ORDER BY p.sharpe_ratio DESC
LIMIT 5;

-- ==========================================
-- Query 4 : Lowest Expense Ratio
-- ==========================================

SELECT
    scheme_name,
    expense_ratio_pct
FROM dim_fund
ORDER BY expense_ratio_pct ASC
LIMIT 5;

-- ==========================================
-- Query 5 : Top Fund Houses by Total AUM
-- ==========================================

SELECT
    f.fund_house,
    ROUND(SUM(a.aum_crore),2) AS total_aum
FROM fact_aum a
JOIN dim_fund f
ON a.fund_id = f.fund_id
GROUP BY f.fund_house
ORDER BY total_aum DESC
LIMIT 10;

-- ==========================================
-- Query 6 : Category-wise Average 5-Year Return
-- ==========================================

SELECT
    f.category,
    ROUND(AVG(p.return_5yr_pct),2) AS avg_return
FROM fact_performance p
JOIN dim_fund f
ON p.fund_id = f.fund_id
GROUP BY f.category
ORDER BY avg_return DESC;

-- ==========================================
-- Query 7 : Risk vs Return
-- ==========================================

SELECT
    f.scheme_name,
    p.return_5yr_pct,
    p.std_dev_ann_pct
FROM fact_performance p
JOIN dim_fund f
ON p.fund_id = f.fund_id
ORDER BY p.return_5yr_pct DESC;

-- ==========================================
-- Query 8 : Top Rated Funds
-- ==========================================

SELECT
    f.scheme_name,
    p.morningstar_rating
FROM fact_performance p
JOIN dim_fund f
ON p.fund_id = f.fund_id
ORDER BY p.morningstar_rating DESC,
         f.scheme_name;

-- ==========================================
-- Query 9 : Expense Ratio vs Return
-- ==========================================

SELECT
    f.scheme_name,
    f.expense_ratio_pct,
    p.return_5yr_pct
FROM dim_fund f
JOIN fact_performance p
ON f.fund_id = p.fund_id
ORDER BY p.return_5yr_pct DESC;

SELECT * FROM fact_transactions
LIMIT 5;