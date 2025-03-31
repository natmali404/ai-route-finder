#SIGMANALIZA TABU SEARCH
############################
# N(s) is the neighbourhood of s, f(s) is the objective function

# algorithm steps:

# generate s0 - starting solution
# current solution s = s0, tabu T = {}, best solution best_s = s
# define neighbourhood N(s)
# until the ending conditions are satisfied:
    # generate neighbourhood of the current solution N(s)
    # we search the entirety of N(s) or we sample it in a deterministic way
    # we choose the best neighbour (si, neigbour that belongs to the neighbourhood but not tabu)
    # T = T + N(s)
    # we set s=si, if f(s) <= f(best_s), then best_s = s
# return best_s

#ending conditions: we define them ourselves
# for example: (len(stop_list)!)-1

#we can use the previously implemented a* algorithm to calculate the cost between the stops in solutions

# cost function = the sum of edge weights. the lower, the better
# if we swap two edges and the total cost decreases, it is a better solution

# t = |T|, fifo, during overflow the oldest solution is removed

# tabu_search(graph, "PL. GRUNWALDZKI", ['Wrocławski Park Przemysłowy', 'Arkady (Capitol)', 'pl. Wróblewskiego'], '12:00', 't')


path, total_travel_time, route_cost = find_a_star_path(graph, "PL. GRUNWALDZKI", "Wrocławski Park Przemysłowy", "15:49", 'manhattan')