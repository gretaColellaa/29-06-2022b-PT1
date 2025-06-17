import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._mapAlbum = {}

    def handleCreaGrafo(self, e):
        try: float(self._view._txtInDurata.value)
        except: self._view.create_alert("inserire un valore valido")

        self._model.crea_grafo(float(self._view._txtInDurata.value))
        self.fillDD()

        self._view.txt_result.controls.append(ft.Text(f"il grafo ha {self._model.getNumNodes()} nodi"
                                                      f" e {self._model.getNumEdges()} archi"))

        self._view.update_page()

    def handleStampa(self, e):
        if self._view._ddAlbum.value:
            self._view.txt_result.clean()
            album = self._mapAlbum[self._view._ddAlbum.value]
            lista_succ = sorted(self._model.stampaAdiacenze(album), key=lambda x:x[1], reverse=True)

            for s, b in lista_succ:

                self._view.txt_result.controls.append(ft.Text(f"{str(s)}, bilancio: {b} (peso archi in minuti)"))
            self._view.update_page()



        else:
            self._view.create_alert("Seleziona un album")




    def handlePercorso(self, e):
        pass

    def fillDD(self):
        album = sorted(self._model._nodes, key=lambda x : x.Title)
        for n in album:
            self._mapAlbum[n.Title] = n
            self._view._ddAlbum.options.append(ft.dropdown.Option(n.Title))

        self._view.update_page()