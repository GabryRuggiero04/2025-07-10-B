import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._lunPath = None
        self._bestPeso = None
        self._bestPath = None
        self._allEdges = None
        self._allNodesId = None
        self._allCategories = None
        self._graph = nx.DiGraph()
        self._allProducts = DAO.getAllProducts()
        self._idMap = {}
        for p in self._allProducts:
            self._idMap[p.product_id] = p



    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        self._allCategories = DAO.getAllCategories()
        return self._allCategories

    def buildGraph(self, date1, date2, categoryId):
        self._graph.clear()
        self._allNodesId = DAO.getAllNodes(categoryId)
        for nodeId in self._allNodesId:
            self._graph.add_node(self._idMap[nodeId])
        self.addEdges(date1, date2, categoryId)

    def addEdges(self, date1, date2, categoryId):
        self._allEdges= DAO.getAllEdges(date1, date2, categoryId)
        for e in self._allEdges:
            if e[2]<e[3] :
                self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=e[2]+e[3])
            elif e[2]>e[3] :
                self._graph.add_edge(self._idMap[e[1]], self._idMap[e[0]], weight=e[2]+e[3])
            else:
                self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=e[2]+e[3])
                self._graph.add_edge(self._idMap[e[1]], self._idMap[e[0]], weight=e[2]+e[3])

    def detailEdges(self):
        return len(self._graph.nodes()),len(self._graph.edges())

    def getGraph(self):
        return self._graph

    def top5(self):
        listaNodoValore = []
        for n in self._graph.nodes():
            valore = 0
            for p in self._graph.predecessors(n):
                peso=self._graph.get_edge_data(p,n,"weight")
                valore += peso["weight"]
            for s in self._graph.successors(n):
                peso=self._graph.get_edge_data(n,s,"weight")
                valore-=peso["weight"]
            listaNodoValore.append((n,valore))
        return listaNodoValore

    def getPath(self, productStart, productEnd, lun):
        self._bestPath=[]
        self._lunPath=lun
        self._bestPeso=0
        self.ricorsione([productStart], productEnd)
        return self._bestPath, self._bestPeso

    def ricorsione(self, parziale, productEnd):
        if len(parziale)==self._lunPath and parziale[-1]==productEnd:
            pesoTot= self.calcoloPeso(parziale)
            if pesoTot>self._bestPeso:
                self._bestPeso=pesoTot
                self._bestPath = copy.deepcopy(parziale)
        else:
            print("qui")
            for n in self._graph.successors(parziale[-1]):
                print(f"Esploro nodo {parziale[-1]}, successori: {list(self._graph.successors(parziale[-1]))}")
                if len(parziale)==(self._lunPath-1):
                    if n==productEnd:
                        if n not in parziale:
                            parziale.append(n)
                            self.ricorsione(parziale, productEnd)
                            parziale.pop()
                else:
                    if n!=productEnd:
                        if n not in parziale:
                            parziale.append(n)
                            self.ricorsione(parziale, productEnd)
                            parziale.pop()


    def calcoloPeso(self, parziale):
        sommaPeso=0
        for n in range (len(parziale)-1):
            sommaPeso+= self._graph.get_edge_data(parziale[n],parziale[n+1])["weight"]
        return sommaPeso

