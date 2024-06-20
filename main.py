import sys
from common import print_tour, read_input
from unionFind import unionFind

def distance(city1, city2):
    return ((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)**0.5
            
# Create a minimum spanning tree 
def create_mst(dist, N):
    edges = []
    for i in range(N):
        for j in range(i+1,N):
            edges.append((dist[i][j],i,j))
    edges.sort()
    uf = unionFind(N)
    mst = [[] for i in range(N)]
    
    for i in range(len(edges)):
        w,u,v = edges[i]
        # Not to create a cycle and not to have more than 2 edges
        if not uf.same(u,v) and len(mst[u]) < 2 and len(mst[v]) < 2:
            mst[u].append(v)
            mst[v].append(u)
            uf.unite(u,v)
    
    # Connect the two nodes with only one edge
    one_edge_node = []
    for i in range(N):
        if len(mst[i]) == 1:
            one_edge_node.append(i)
            
    # Check if there are two nodes with only one edge
    #To do : 葉が2個とは限らない
    if len(one_edge_node) >= 2:
        mst[one_edge_node[0]].append(one_edge_node[1])
        mst[one_edge_node[1]].append(one_edge_node[0])

    return mst

# Create a path from the minimum spanning tree
def create_path(dist,mst,N):
    visited = set()
    current = 0
    path = [current]
    visited.add(current)
    
    while len(path) < N:
        next_node = mst[current][0]
        if next_node in visited:
            #To do : ここでmst[current][1]の確認ができていない
            next_node = mst[current][1]
        visited.add(next_node)
        path.append(next_node)
        current = next_node
    print(path)
    return path

        
# 2-opt algorithm to improve the solution
def two_opt(tour, dist):
    N = len(tour)
    while True:
        count = 0
        for i in range(N-2):
            for j in range(i+2, N):
                l1 = dist[tour[i]][tour[i + 1]]
                l2 = dist[tour[j]][tour[(j + 1) % N]]
                l3 = dist[tour[i]][tour[j]]
                l4 = dist[tour[i + 1]][tour[(j + 1) % N]]
                if l1 + l2 > l3 + l4:
                    tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                    count += 1
        if count == 0:
            break
    return tour

#or-1pt algorithm to improve the solution
def or_opt(tour, dist):
    N = len(tour)
    while True:
        count = 0
        for i in range(N):
            i0 = i
            i1 = (i + 1) % N
            i2 = (i + 2) % N
            for j in range(N):
                j0 = j
                j1 = (j + 1) % N
                if j0 not in {i0, i1}:
                    l1 = dist[tour[i0]][tour[i1]]
                    l2 = dist[tour[i1]][tour[i2]]
                    l3 = dist[tour[j0]][tour[j1]]
                    l4 = dist[tour[j0]][tour[i1]]
                    l5 = dist[tour[j1]][tour[i1]]
                    l6 = dist[tour[i0]][tour[i2]]
                    if l1 + l2 + l3 > l4 + l5 + l6:
                        city = tour.pop(i1)
                        if i1 < j1:
                            tour.insert(j0, city)
                        else:
                            tour.insert(j1, city)
                        count += 1
        if count != 0:
            is_improved = True
        else:
            is_improved = False
        if not is_improved:
            break
    print(tour)
    return tour
                    
            
        
   


def solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    mst = create_mst(dist, N)
    tour = create_path(dist,mst,N)
    tour = two_opt(tour, dist)
    tour = or_opt(tour, dist)

    
    return tour
            
  
if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    #print_tour(tour)