import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory. It constructs names, people and movies.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    
    # Get the source and the target
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    # Find solution
    path = shortest_path(source, target)

    # If there is no solution:
    if path is None:
        print("Not connected.")
    else:
        # Number of steps
        degrees = len(path) 
        print(f"{degrees} degrees of separation.")
        # Add the first step, with is from None to the source (Initial State)
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"] # Find the name of the person with id = path[i][1]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"] # Find the title of the movie in which peopla starred in with id = path[i + 1][0]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")



def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    
    # Initialize the frontier to start from the initial state
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    
    # Initialize an empty explored set
    explored = set()
    
    # Keep looping until a solution is found
    while True:
        # If the frontier is empty:
        if frontier.empty():
            return None
        # BFS will chose a node
        node = frontier.remove()
        
        # If node is the solution:
        if node.state == target:
            solution = []
            while node.parent is not None:
                solution.append((node.action, node.state))
                node = node.parent
            return solution[::-1]
        
        # Mark node as explored
        explored.add(node.state)
        
        # Check neighbors and add them to frontier
        for action, state in neighbors_for_person(node.state):
            if state not in explored and not frontier.contains_state(state):
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

if __name__ == "__main__":
    main()
