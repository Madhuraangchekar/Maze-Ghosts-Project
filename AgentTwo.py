# ===========================================================================
# Agent Two 
# ===========================================================================
# 0   = Empty Space
# 1   = Blocked Wall
# 100 = Empty Space with ghost
# 200 = Blocked Wall with ghost
# ===========================================================================
import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from GhostSimulation import *
from BFS import *
from Maze import *
from time import time
from datetime import datetime
import csv

def agent_two():
    start = time()
    print("Started...")
    n_ghost = 200
    n_row = 51
    n_col = 51
    walk = [[0, 1],
            [0, -1],
            [1, 0],
            [-1, 0]]

    filename_txt="Results/AgentTwo/Run 1.txt"
    filename_csv="Results/AgentTwo/Run 1.csv"
    file=open(filename_txt,"a")
    csvfile = open(filename_csv, "a")
    csv_writer=csv.writer(csvfile)
    fields=['Date Time','Ghost Number','Number of Mazes','Time Taken','Survived','Hanged','Died','Comments']
    csv_writer.writerow(fields)
    time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
    file = open("Results/AgentTwo/Run 1.txt", "a")
    text = "\n\n\n======  Start Time  =========->  " + \
        datetime.now().strftime("%m/%d/%y %H:%M:%S")
    csv_writer.writerow(["Execution Started "+text])
    file.write(text)
    file.write("\nNo. of Ghosts = %d" % n_ghost)
    file.write("\nNo. of mazes for each ghost = 100")

    for i_ghost in range(1, n_ghost+1, 5):
        gh_st_time=time()
        n_maze = 1
        n_alive_for_this_ghost = 0
        n_dead_for_this_ghost = 0
        node_reached = []
        print("Ghost Number ", i_ghost, " Started")
        gh_time=time()
        while (n_maze > 0):
            n_maze -= 1
            maze = generate_maze(n_row, n_col, True)[0]
            ghost_position = list()
            # Spawning Ghosts at random location
            spawn_ghosts(maze, i_ghost, n_row, n_col, ghost_position)
            get_init_path = get_bfs_path(maze, n_row, n_col, (0, 0), True)
            is_init_path_valid = get_init_path[0]
            path = list()
            if is_init_path_valid:
                path.append(get_init_path[1].pop(1))
            else:
                ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost(
                    walk, ghost_position, n_row, n_col, maze, 0, 0)
                path.append((play_next_r, play_next_c))
              
            # ========================================================================================================================================
            # ===============================       Player Starts Moving       =========================================================================
            # ========================================================================================================================================
            for play_pos_r, play_pos_c in path:
                is_player_alive = True

                if maze[play_pos_r][play_pos_c] >= 100:
                    is_player_alive = False
                    break
                if (play_pos_r, play_pos_c) == (n_row-1, n_col-1):
                    break
                # ===============================      Ghost Simulation       =========================================================================
                maze, ghost_position = ghost_simulation(
                    walk, ghost_position, n_row, n_col, maze)
                # ===========================================================================

                # Now all ghosts are in their next position. So if player is on the same cell, they die
                if maze[play_pos_r][play_pos_c] >= 100:
                    # player dies
                    is_player_alive = False
                    node_reached.append((play_pos_r, play_pos_c))
                    break

                if (play_pos_r, play_pos_c) == (n_row-1, n_col-1):
                    # player survives
                    break

                # ===================================================================================================
                # Now this code will execute only if player hasn't yet died. so player will have to replan the path
                # ===================================================================================================
                latest_path = get_bfs_path(
                    maze, n_row, n_col, (play_pos_r, play_pos_c), True)
                # contains True/False : if there exists a path from player to goal,
                if latest_path[0]:
                    # append the next cell in the path
                    path.append(latest_path[1].pop(1))
                elif latest_path[0] == False:
                    # Path is blocked by ghost. Run away..We find the nearest ghost to current player position.
                    # Then select the next direction which is the farthest from this particular ghost
                    ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost(
                        walk, ghost_position, n_row, n_col, maze, play_pos_r, play_pos_c)
                    path.append((play_next_r, play_next_c))

                   
            if is_player_alive:
                n_alive_for_this_ghost += 1
                # print("Alive")
            else:
                n_dead_for_this_ghost += 1
              
        now=time()
        file.write("\nReport for %d Number of Ghosts" % i_ghost)
        file.write("\nPlayer Survivability =           %d" % n_alive_for_this_ghost+" %")
        file.write("\nTime taken for this ghost : "+str(now-gh_time)+" s")
        print("Time taken for this ghost : "+str(now-gh_time)+" s")
        print("Total Time till now: "+str(now-start)+" s")
        print("Ghost Number ", i_ghost, " Done\n")
        gh_end_time=time()

        #  fields=['Date Time','Ghost Number','Maze Number','Time Taken','Survived','Hanged','Died','Comments']
        time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
        csv_writer.writerow([time_now,i_ghost,100,str(gh_end_time-gh_st_time),str(n_alive_for_this_ghost),0,str(n_dead_for_this_ghost)])
        
    end = time()
    file.write("\n\nExecution Time = "+str(end-start)+" s")
    print("Execution time : "+str(end-start)+" s")
    file.close()
    print("Done!")


agent_two()
