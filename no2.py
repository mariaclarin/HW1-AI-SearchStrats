import random

#the graph with each nodes, connected neighbors, and the respective weights
graph = {
    'a': {'b': 12, 'c': 10, 'g': 12}, #start
    'b': {'a': 12, 'c': 8, 'd': 12},
    'c': {'a': 10, 'b': 8, 'd': 11, 'g': 9, 'e': 3},
    'd': {'b': 12, 'c': 11, 'e': 11, 'f': 10},
    'e': {'c': 3, 'd': 11, 'f': 6, 'g': 7},
    'f': {'d': 10, 'e': 6, 'g': 9},
    'g': {'a': 12, 'c': 9, 'e': 7, 'f': 9}
}

#function to calculate the total distance of the route, 
#based on the weights of distance taken between each node that is traversed
def calcRouteDistance(route):
    distance = 0
    #for loop traverse through each city in the path once and creating the route until it returns to starting point (a)
    for i in range(len(route) - 1):
        #adds the distance of the weights of the next neighbor node (.get(route[i + 1]) from the current node (graph[route[i]])
        distance += graph[route[i]].get(route[i + 1], float('inf')) 
    #exit the loop and adds the final distance as we have returned to the starting point (graph[route[-1]])
    distance += graph[route[-1]].get(route[0], float('inf')) 
    return distance

#all the keys in the graph will be put in a list named cities 
#cities = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
cities = list(graph.keys())

#variables to store parameters of the genetic algo, is mutable
noOfGenerations = 1000
populationSize = 100
rateOfMutation = 0.05 #between 0 and 1

#using random.sample() to generate permutations of the routes (randomized), in which each city is visited once 
routes = [random.sample(cities, len(cities)) for _ in range(populationSize)]

#manually set and ensuring the starting point to 'a'
for i in range(populationSize):
    routes[i].remove('a') #remove any i instance of 'a'
    routes[i].insert(0, 'a') #inserts a in index 0, ensuring that 'a' will be at the start of the list

#GENETIC ALGORITHM LOOP
for generation in range(noOfGenerations):
    #calculate the fitnesss score of each route
    fitnessScore = [(route, calcRouteDistance(route)) for route in routes]
    #sort them by route length
    fitnessScore.sort(key=lambda x: x[1])  

    #select top routes for genetic algorithm generation process
    selectedRoutes = [route for route, _ in fitnessScore[:populationSize // 2]]
    #copy to apply genetic algorithm (crossover and mutation)
    newGeneration = selectedRoutes.copy()

    #while loop that runs until it reaches the population size
    while len(newGeneration) < populationSize:
        parent1, parent2 = random.sample(selectedRoutes, 2)
        crossoverPoint = random.randint(1, len(cities) - 1) #random point of crossover between the two parents above
        #takes the route of parent1 until the point, and iterates through parent2 for cities that are not already in the parent1 traversal
        child = parent1[:crossoverPoint] + [city for city in parent2 if city not in parent1[:crossoverPoint]]

        if random.random() < rateOfMutation:
            mutationIndices = random.sample(range(len(cities)), 2) #take two random cities that will be swapped
            child[mutationIndices[0]], child[mutationIndices[1]] = child[mutationIndices[1]], child[mutationIndices[0]] #swapping the two values in the child
        newGeneration.append(child) #adding the child route to the new generation/routes

    routes = newGeneration


#the route that is best, will have the best fitness score
best_route, best_distance = fitnessScore[0]


print("Shortest Possible Route:", best_route)
print("Total Distance:", best_distance)

print('NOTES ==================================================================')
print('The best route doesnt include the final position because its a repeat of the starting point.')
print('But if we compare with the graph it will always start from city a and end up in city a.')
print('The total distance also includes the addition of the distance between the last city visited to city a')