from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAlbums(dMin):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """ SELECT a.AlbumId, a.Title, a.ArtistId, sum(t.Milliseconds)/1000/60 as dTot
                           from album a, track t
                           where a.AlbumId = t.AlbumId 
                           GROUP BY a.AlbumId 
                           HAVING dTot > %s """

        cursor.execute(query, (dMin,))  # in minuti

        results = []
        for row in cursor:
            results.append(Album(**row))

        cursor.close()
        cnx.close()
        return results

