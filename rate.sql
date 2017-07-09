SELECT sentence_type, (number*1.0/time_period) as rate
	FROM
		(SELECT sentence_type, count(*) as number
			FROM sentences
			GROUP BY sentence_type),
		(SELECT MAX(strftime('%s',date))-MIN(strftime('%s',date)) as time_period
			FROM sentences)
