import pandas as pd
import MySQLdb

sql_con = MySQLdb.connect(host='104.196.212.179', port=3306,
                          user='root', passwd='data620pw',
                          db='billsdata')

members = pd.read_sql('SELECT name AS Name FROM members;', con=sql_con)
sponsorships = pd.read_sql('SELECT cs.name AS Source, s.name AS Target '
                           'FROM sponsors AS s INNER JOIN cosponsors AS cs '
                           'ON s.billID = cs.billID;', con=sql_con) 

sql_con.close()

import networkx as nx

nodes = list(members.values.flatten())
edges = [tuple(x) for x in sponsorships.to_records(index=False)]

G = nx.DiGraph()

G.add_nodes_from(nodes)
G.add_edges_from(edges)

nx.draw(G, with_labels=False)

nx.write_gexf(G, "senators114.gexf")
