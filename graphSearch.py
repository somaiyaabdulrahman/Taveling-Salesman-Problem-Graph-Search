
def read_graph(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith("TOTAL LOCATIONS:") and not line.startswith("LOCATIONS AND DISTANCES:"):
                city1, city2, distance = line.split()
                distance = int(distance)
                if city1 not in graph:
                    graph[city1] = []
                if city2 not in graph:
                    graph[city2] = []
                graph[city1].append((city2, distance))
                graph[city2].append((city1, distance))
    return graph

def bellman_ford(graph, destination):
    # Step 1: Initialize distances and previous cities
    distance = {city: float('inf') for city in graph}
    previous_city = {city: None for city in graph}

    # The distance from the source to itself is zero
    distance[destination] = 0

    # Step 2: Relax edges repeatedly
    for _ in range(len(graph) - 1):
        for current_city in graph:
            for neighbor, w in graph[current_city]:
                if distance[current_city] + w < distance[neighbor]:
                    distance[neighbor] = distance[current_city] + w
                    previous_city[neighbor] = current_city

    # Step 3: Check for negative-weight cycles
    for current_city in graph:
        for neighbor, w in graph[current_city]:
            if distance[current_city] + w < distance[neighbor]:
                raise ValueError("Graph contains a negative weight cycle")

    return distance, previous_city

def reconstruct_path(previous_city, destination, city):
    path = []
    current = city
    while current != destination:
        if current is None:
            return None  # No path found
        path.insert(0, current)
        current = previous_city[current]
    path.insert(0, destination)
    return path

file_path = 'city 1.txt'
graph = read_graph(file_path)
sorted_graph = sorted(graph)

destination = 'F'

distances, previous_city = bellman_ford(graph, destination)

# If the graph does not contain a negative weight cycle, print the shortest paths
if distances:
    print(f"Shortest distances from each city to {destination}:")
    for city in sorted_graph:
        if city != destination:
            print(f"Distance from {city} to {destination}: {distances[city]}")

    print(f"\nShortest paths from each city to {destination}:")
    for city in sorted_graph:
        if city != destination:
            path = reconstruct_path(previous_city, destination, city)
            if path:
                print(f"Path from {destination} to {city}: {path}")
else:
    print("The graph contains a negative weight cycle.")

