from domain import SimpleDirectedGraph
from Djkstra import run_dijkstra_analysis
from UCS import run_ucs_analysis
from UCS2 import run_ucs_analysis2

g = SimpleDirectedGraph.create_from_file('input.txt')

end = '12310'
start = '12914'
print("Dijkstra :")
run_dijkstra_analysis(g,start,end)
print("*" *130)
print("UCS1 :")
run_ucs_analysis(g, start, end)
print("*" *130)
# print("UCS2 :")
# run_ucs_analysis2(g,start,end)

