import argparse
import sys
from wgc import *

if __name__ == "__main__":
    p = argparse.ArgumentParser(prog="WGC Solver", 
                                description="Solves the WGC with the chosen algorithim, displaying results.")
    p.add_argument("-a", "--algorithm", help="The algorithm (IDS or BFS) to use.", type=str)

    ITER_1 = Node()
    ITER_1.left_river.add("farmer")
    ITER_1.left_river.add("goat")
    ITER_1.left_river.add("cabbage")
    ITER_1.left_river.add("wolf")

    ITER_2 = Node()
    ITER_2.right_river.add("farmer")
    ITER_2.right_river.add("goat")
    ITER_2.left_river.add("cabbage")
    ITER_2.left_river.add("wolf")

    parsed = p.parse_args(sys.argv[1::])
    if (parsed.algorithm.upper() == "BFS"):
        b = BFS()
        p = b.MAIN(ITER_1)
        print(p)
        print_solution_path(ITER_1, p.solution_path)
        b = BFS()
        p = b.MAIN(ITER_2)
        print(p)
        print_solution_path(ITER_2, p.solution_path)
    elif (parsed.algorithm.upper() == "IDS"):
        d = IDS()
        p = d.MAIN(ITER_1, 10)
        print(p)
        print_solution_path(ITER_1, p.solution_path)
        d = IDS()
        p = d.MAIN(ITER_2, 10)
        print(p)
        print_solution_path(ITER_2, p.solution_path)
    else:
        print("Invalid algorithm")