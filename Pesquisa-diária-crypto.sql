SELECT c.id as ID,
       c.register_date as SnapShot_Date,
       c.usd as Current_Price_USD,
       ((SELECT c.usd from `data-case-study-322621.analytics_engineer_case.crypto` as c where date(c.register_date)= current_date())-(SELECT c.usd  from `data-case-study-322621.analytics_engineer_case.crypto` as c where date(c.register_date)= DATE_SUB(current_date(), INTERVAL 7 DAY))),
	   ((SELECT c.usd from `data-case-study-322621.analytics_engineer_case.crypto` as c where date(c.register_date)= current_date())-(SELECT c.usd  from `data-case-study-322621.analytics_engineer_case.crypto` as c where date(c.register_date)= DATE_SUB(current_date(), INTERVAL 14 DAY))),
	   c.usd_market_cap as Market_cap_USD,
	   ((SELECT c.usd_market_cap from `data-case-study-322621.analytics_engineer_case.crypto` as c where date(c.register_date)= current_date())-(SELECT c.usd_market_cap  from `data-case-study-322621.analytics_engineer_case.crypto` as c where date(c.register_date)= DATE_SUB(current_date(), INTERVAL 7 DAY))),
       ((SELECT c.usd_market_cap from `data-case-study-322621.analytics_engineer_case.crypto` as c where date(c.register_date)= current_date())-(SELECT c.usd_market_cap  from `data-case-study-322621.analytics_engineer_case.crypto` as c where date(c.register_date)= DATE_SUB(current_date(), INTERVAL 14 DAY))),

 FROM `data-case-study-322621.analytics_engineer_case.crypto` as c LIMIT 1000
