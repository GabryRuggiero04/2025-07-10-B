from datetime import datetime

from model import model
myModel=model.Model()
myModel.buildGraph(datetime(2016,1,1),datetime(2018,12,28),5)
numNodes, numEdges=myModel.detailEdges()
print(numNodes)
print(numEdges)