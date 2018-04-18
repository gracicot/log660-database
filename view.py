import sqlite3

conn = sqlite3.connect('./db/Labo2.db')

conn.enable_load_extension(True)
conn.load_extension('./db/maths')

c = conn.cursor()

c.execute('''

CREATE VIEW Correlation AS
SELECT cotes.idFilm as thisFilmid, cotes2.idFilm as otherFilmid,
(Select SUM(
			((coteClient.cote - averagesezz.coteFilm1) * (coteClient2.cote - averagesezz.coteFilm2))
			/SQRT(clientCalcData.calcClient1 * clientCalcData.calcClient2)
		)
	from cotes as coteClient, 
	
		(select 
				SUM((coteClient.cote - averagesezz.coteFilm1) * (coteClient.cote - averagesezz.coteFilm1)) as calcClient1,
				SUM((coteClient2.cote - averagesezz.coteFilm2) * (coteClient2.cote - averagesezz.coteFilm2)) as calcClient2
				
			from cotes as coteClient join cotes as coteClient2
			on coteClient.idClient = coteClient2.idClient
			Where coteClient.idFilm = cotes.idFilm and coteClient2.idFilm = cotes2.idFilm
			group by coteClient.idFilm, coteClient2.idFilm
		) as clientCalcData
		
	join cotes as coteClient2
	on coteClient.idClient = coteClient2.idClient
	Where coteClient.idFilm = cotes.idFilm and coteClient2.idFilm = cotes2.idFilm
	group by coteClient.idFilm, coteClient2.idFilm
) as  correlation
From cotes join cotes as cotes2
ON cotes.idFilm <> cotes2.idFilm AND cotes.idClient = cotes2.idClient
join (
SELECT avg(cotesavg.cote) as coteFilm1, avg(cotes2avg.cote) as coteFilm2, cotesavg.idFilm as idFilm1, cotes2avg.idFilm as idFilm2
from cotes as cotesavg
join cotes as cotes2avg
ON cotesavg.idFilm <> cotes2avg.idFilm AND cotesavg.idClient = cotes2avg.idClient
Where cotesavg.idFilm > cotes2avg.idFilm 
GROUP BY  cotesavg.idFilm, cotes2avg.idFilm

) as averagesezz on cotes.idFilm = averagesezz.idFilm1 and cotes2.idFilm = averagesezz.idFilm2
Where cotes.idFilm > cotes2.idFilm  and correlation >= 0
GROUP BY  cotes.idFilm, cotes2.idFilm
having Count(cotes.idClient) > 50;

''')
