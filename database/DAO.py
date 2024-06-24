from database.DB_connect import DBConnect
from model.album import Album
from model.connessione import Connessione


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNodi(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.*
from album a ,track t 
where a.AlbumId =t.AlbumId 
group by a.AlbumId 
having sum(t.Milliseconds)>%s
order by a.Title"""

        cursor.execute(query,(durata,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni(n):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.a1 as v1, t2.a2 as v2, t1.d1 as t1, t2.d2 as t2, (t1.d1+t2.d2) as peso
from (select t.AlbumId as a1, sum(t.Milliseconds) as d1
from track t 
group by t.AlbumId 
having sum(t.Milliseconds)>%s) as t1,(select t.AlbumId as a2, sum(t.Milliseconds) as d2
from track t 
group by t.AlbumId 
having sum(t.Milliseconds)>%s) as t2
where t1.a1<t2.a2 and t1.d1!=t2.d2 and (t1.d1+t2.d2)>4*%s"""

        cursor.execute(query,(n,n,n,))

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result

