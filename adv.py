import pdb
from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
backtrack_path = []
rooms = {}

# start here

# make function that flips direction for backtrack_path


def flip_direction(dir):
    if dir == "n":
        return "s"
    if dir == "s":
        return "n"
    if dir == "w":
        return "e"
    if dir == "e":
        return "w"


# put the first room in the dictionary with the list of exits
rooms[player.current_room.id] = player.current_room.get_exits()
# print(rooms)

# while length of visited rooms is less than rooms in graph - the first room
while len(rooms) < len(room_graph)-1:
    # if current room never visited:
    if player.current_room.id not in rooms:
        # set exits list to the visited room dict
        rooms[player.current_room.id] = player.current_room.get_exits()
        # print("rooms updated", rooms)
        # mark the room you came from as explored so remove from exits
        last_room = backtrack_path[-1]
        rooms[player.current_room.id].remove(last_room)
        # print("removed room just visited", rooms)
    # if theres a dead end:
    while len(rooms[player.current_room.id]) < 1:
        # remove last direction from backtrack
        backtrack = backtrack_path.pop()
        # travel back
        player.travel(backtrack)
        # add move to traversal path
        traversal_path.append(backtrack)
        # print("backtracked", traversal_path)
    # if there are unexplored rooms:
    else:
        # pick the last exit direction using pop
        last_exit = rooms[player.current_room.id].pop()
        # add move to traversal path
        traversal_path.append(last_exit)
        # print("moved forward", traversal_path)
        # store the reverse direction for going back to backtrack_path
        backtrack_path.append(flip_direction(last_exit))
        # print("backtrack path updated", backtrack_path)
        # travel to next room
        player.travel(last_exit)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
