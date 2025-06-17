import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):

        self._nodes = []
        self._edges = []
        self._grafo = nx.DiGraph()

        self._idMapAlbum = {}
        pass


    def crea_grafo(self, durata):
        print("crea_grafo chiamata")
        self._nodes = DAO.getAlbums(durata)
        print("nodi ok")

        for n in self._nodes:
            self._idMapAlbum[n.AlbumId] = n
            for n2 in self._nodes:
                if n!= n2 and n.dTot!=n2.dTot and (n.dTot+n2.dTot)>4*durata:
                    if (n,n2) not in self._edges and (n2,n) not in self._edges:
                        if n.dTot>n2.dTot:
                            self._edges.append((n2,n,{'weight': n.dTot+n2.dTot}))
                        else:
                            self._edges.append((n, n2, {'weight': n.dTot + n2.dTot}))

        print("edges ok")
        self._grafo.add_nodes_from(self._nodes)

        self._grafo.add_edges_from(self._edges)



    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)


    def getBilancio(self, album):
        peso_uscenti = sum(data["weight"] for _, _, data in self._grafo.out_edges(album, data=True))
        peso_entranti = sum(data["weight"] for _, _, data in self._grafo.in_edges(album, data=True))
        bilancio = peso_entranti-peso_uscenti
        return bilancio

    def stampaAdiacenze(self, album):
        successori = self._grafo.successors(album)

        lista_succ = []
        for s in successori:
            #print(s.Title)
            bilancio_s = self.getBilancio(s)
            lista_succ.append((s, bilancio_s))


        return lista_succ


