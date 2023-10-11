#defining the possible moves as a tree adjacency, (row, column) : [list of possible moves]
moves = {
    'S':['1,0'],
    '1,0':['2,0'],
    '2,0':['3,0'],
    '3,0':['4,0','3,1'],
    '4,0':[],
    '3,1':['2,1', '3,2', '4,1'],
    '2,1':['1,1'],
    '1,1':['0,1'],
    '0,1':['0,2'],
    '0,2':['0,3'],
    '0,3':['1,3'],
    '1,3':['G', '2,3'],
    'G':[],
    '2,3':['2,2'],
    '2,2':[],
    '3,2':[],
    '4,1':['4,2'],
    '4,2':['4,3'],
    '4,3':['4,4'],
    '4,4':['3,4'],
    '3,4':['2,4','3,3'],
    '2,4':['2,3', '1,4'],
    '3,3':[],
    '1,4':['0,4'],
    '0,4':[]
}


visited =[]

#function for dfs (depth first search)
def dfs(moves, node, goal):
    if node not in visited:
        print(node)
        visited.append(node) #add each node that is visited in the set
        if node == goal:
            print('Goal Node Found!')
            return True #if goal node is found, exit and return True
        for neighbor in moves.get(node, []):
            if dfs(moves, neighbor, goal): #recursively call the function for the neighboring node
                return True #if goal node is already found, exit and return true
    return False #goal node is not found

#function for bfs (breadth first search)
def bfs(moves, start, goal):
    #queue data structure
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node == goal:
            print(node)
            print('Goal Node Found!')
            visited.append(node) #add the node that we visited to the set

            break  #exit the loop because the goal node is found
        if node not in visited:
            print(node)
            visited.append(node) #add the node that we visited to the set
            queue.extend(neighbor for neighbor in moves.get(node, []) if neighbor not in visited) #extend the queue for nodes that are not already visited


#DFS and BFS for 'S' starting node to find 'G' goal node
print("Depth First Search (DFS):")
dfs(moves, 'S', 'G')

visited = [] #empty the list for BFS

print("\nBreadth First Search (BFS):")
bfs(moves, 'S', 'G')

