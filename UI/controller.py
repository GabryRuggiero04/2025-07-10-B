import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._ProductEndSelectedValue = None
        self._ProductStartSelectedValue = None
        self._categorySelectedValue = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDCategory(self):
        allCategories = self._model.getCategories()
        for c in allCategories:
            self._view._ddcategory.options.append(
                ft.dropdown.Option(data=c,
                                   text=c.category_name,
                                   key=c.category_id,
                                   on_click= self.categoryChoice)
            )

    def categoryChoice(self, e):
        self._categorySelectedValue= e.control.data
        return self._categorySelectedValue

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        categoria= self._categorySelectedValue
        if self._view._ddcategory.value is None:
            self._view.create_alert("Scegliere una categoria dal menù a tendina!!")
            return
        dataStart= self._view._dp1.value
        dataEnd= self._view._dp2.value
        if (dataStart is None):
            self._view.create_alert("Scegliere data start!!")
            return
        if (dataEnd is None):
            self._view.create_alert("Scegliere data end!!")
            return
        if dataStart > dataEnd:
            self._view.create_alert("La data di start deve precedere la data di end!!")
            return
        self._view.txt_result.controls.append(
            ft.Text("Date selezionate: ", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Start: {dataStart.date()}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"End: {dataEnd.date()}")
        )
        self._model.buildGraph(dataStart,dataEnd, categoria.category_id)
        numNodes, numEdges = self._model.detailEdges()
        if numEdges<0 or numNodes<0:
            self._view.txt_result.controls.append(
                ft.Text("Grafo vuoto o creato in modo errato!!", color="red")
            )
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.append(
                ft.Text("Grafo creato correttamente", color="green")
            )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {numNodes}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {numEdges}")
        )
        grafo= self._model.getGraph()
        nodesList= list(grafo.nodes())
        for n in nodesList:
            self._view._ddProdStart.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.product_id,
                                   text=n.product_name,
                                   on_click=self.choiceProductStart)
            )
            self._view._ddProdEnd.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.product_id,
                                   text=n.product_name,
                                   on_click=self.choiceProductEnd)
            )
        self._view.update_page()

    def choiceProductStart(self,e):
        self._ProductStartSelectedValue= e.control.data
        return self._ProductStartSelectedValue

    def choiceProductEnd(self,e):
        self._ProductEndSelectedValue= e.control.data
        return self._ProductEndSelectedValue

    def handleBestProdotti(self, e):
        lista= self._model.top5()
        lista.sort(key=lambda x: x[1], reverse=True)
        self._view.txt_result.controls.append(
            ft.Text("I 5 prodotti più venduti sono: ", color="green")
        )
        top=5
        if len(lista)<top:
            top=len(lista)
        for t in range (top):
            self._view.txt_result.controls.append(
                ft.Text(f"{lista[t][0]} with score {lista[t][1]}")
            )
        self._view.update_page()

    def handleCercaCammino(self, e):
        self._view.txt_result.controls.clear()
        productStart = self._ProductStartSelectedValue
        productEnd = self._ProductEndSelectedValue
        if self._view._ddProdStart.value is None:
            self._view.create_alert("Scegliere un prodotto di partenza!!")
            return
        if self._view._ddProdEnd.value is None:
            self._view.create_alert("Scegliere un prodotto di arrivo!!")
            return
        lun= self._view._txtInLun.value
        if lun=="":
            self._view.create_alert("Inserire lunghezza del cammino!!")
            return
        try:
            lunInt=int(lun)
        except ValueError:
            self._view.create_alert("Inserire un numero intero come lunghezza del cammino!!")
            return
        if lunInt < 0:
            self._view.create_alert("Inserire un numero positivo come la lunghezza del cammino!!")
            return
        pathNodes, sumWeight= self._model.getPath(productStart,productEnd, lunInt)
        if len(pathNodes)<1:
            self._view.txt_result.controls.append(
                ft.Text(f"Nessun cammino trovato da {productStart} a {productEnd} con lunghezza {lunInt} passi", color="red")
            )
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino da ({productStart}) a ({productEnd}) con lunghezza {lunInt} passi trovato", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Peso totale del cammino: {sumWeight}", color="green")
        )
        for n in pathNodes:
            self._view.txt_result.controls.append(
                ft.Text(n)
            )
        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
