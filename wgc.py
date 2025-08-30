import copy

class Result():
    def __init__(self):
        self.nodes_generated = 0
        self.nodes_expanded = 0
        self.maximum_frontier_size = 0
        self.solution_depth = 0
        self.solution_cost = 0
        self.solution_path = []
        self.type = ""
    def __str__(self):
        return f"Result Type: {self.type} \
                \nNodes Generated: {self.nodes_generated} | Nodes Expanded: {self.nodes_expanded} | Max Frontier Size: {self.maximum_frontier_size} \
                \nSolution Depth: {self.solution_depth} | Solution Cost: {self.solution_cost} | Solution Path: {self.solution_path}"

class Node():
    def __init__(self):
        self.left_river = set()
        self.right_river = set()
        self.prev_actions = []
        self.depth = 0
    def __eq__(self, other):
        other : Node
        return self.left_river == other.left_river and self.right_river == other.right_river
    def transition(self, a):
        pass
    def is_valid(self):
        for side in [self.left_river, self.right_river]:
            # if the side is attended, they won't eat each other
            if "farmer" in side:
                continue

            # the goat cannot be left with the cabbage or the goat
            if "goat" in side and ("cabbage" in side or "wolf" in side):
                return False
        return True

    def actions(self):
        actions = []
        if not self.is_valid():
            return actions

        if "farmer" in self.left_river:
            # we are on the left side
            for x in self.left_river:
                actions.append(x)
        else:
            # we are on the right side
            for x in self.right_river:
                actions.append(x)
        actions.append("")
        actions.remove("farmer")
        return actions
    def __str__(self):
        return str(self.left_river) + " " + str(self.right_river)
class BFS():
    def __init__(self):
        self.queue = []
        self.goal = Node()
        self.goal.right_river.add("farmer")
        self.goal.right_river.add("goat")
        self.goal.right_river.add("cabbage")
        self.goal.right_river.add("wolf")
        self.explored = set()
        self.r = Result()
    def ENQUEUE(self, item):
        self.queue.append(item)
        self.r.nodes_generated += 1
        if len(self.queue) > self.r.maximum_frontier_size:
            self.r.maximum_frontier_size = len(self.queue)
    def DEQUEUE(self):
        return self.queue.pop()
    def GOAL_TEST(self, n):
        return n == self.goal
    def MAIN(self, s0) -> Result:
        self.r = Result()
        self.queue = []
        self.ENQUEUE(s0)
        self.explored = []
        while self.queue:
            n = self.DEQUEUE()
            if self.GOAL_TEST(n):
                n : Node
                self.r.solution_path = n.prev_actions
                self.r.solution_cost = len(n.prev_actions)
                self.r.solution_depth = n.depth
                self.r.type = "WIN"
                return self.r
            self.explored.append(n)
            self.r.nodes_expanded += 1
            for a in n.actions():
                s_ = TRANSITION(n, a)
                if s_ not in self.queue and s_ not in self.explored:
                    self.ENQUEUE(s_)
                    s_.depth += 1
        self.r.type = "FAIL"
        return self.r
    
class DLS():
    def __init__(self):
        self.queue = []
        self.goal = Node()
        self.goal.right_river.add("farmer")
        self.goal.right_river.add("goat")
        self.goal.right_river.add("cabbage")
        self.goal.right_river.add("wolf")
        self.r = Result()
    def PUSH(self, item):
        self.queue.append(item)
        self.r.nodes_generated += 1
        if len(self.queue) > self.r.maximum_frontier_size:
            self.r.maximum_frontier_size = len(self.queue)
    def POP(self):
        return self.queue.pop()
    def GOAL_TEST(self, n):
        return n == self.goal
    def MAIN(self, s0, L) -> Result:
        self.r = Result()
        self.queue = []
        self.PUSH(s0)
        cutoff = False
        while self.queue:
            n = self.POP()
            if self.GOAL_TEST(n):
                self.r.solution_path = n.prev_actions
                self.r.solution_cost = len(n.prev_actions)
                self.r.solution_depth = n.depth
                self.r.type = "WIN"
                return self.r
            if n.depth == L:
                cutoff = True
                continue
            self.r.nodes_expanded += 1
            A = n.actions()
            for a in A[::-1]:
                s_ = TRANSITION(n, a)
                s_.depth += 1
                self.PUSH(s_)
        self.r.type = "CUTOFF" if cutoff else "FAIL"
        return self.r
    
class IDS(DLS):
    def MAIN(self, s0, max_depth):
        for x in range(max_depth):
            r = super().MAIN(s0, x)
            if r.type == "WIN" or r.type == "FAIL":
                return r
        r = Result()
        r.type = "FAIL"
        return r
def TRANSITION(n, a):
    n_ = copy.deepcopy(n)
    n_ : Node
    if "farmer" in n_.left_river:
        if a and a in n_.left_river:
            n_.left_river.remove(a)
            n_.right_river.add(a)
        n_.left_river.remove("farmer")
        n_.right_river.add("farmer")
    elif "farmer" in n_.right_river:
        if a and a in n_.right_river:
            n_.right_river.remove(a)
            n_.left_river.add(a)
        n_.right_river.remove("farmer")
        n_.left_river.add("farmer")
    n_.prev_actions.append(a)
    return n_

def print_solution_path(inital_state, actions_to_sol):
    s = copy.deepcopy(inital_state)
    print("Initial State:", s)
    print("Solution Steps:")
    for x in actions_to_sol:
        s = TRANSITION(s, x)
        if x:
            print("The farmer moved with", x, "to the other side. New state:", s)
        else:
            print("The farmer moved to the other side. New state:", s)
    print("Reached goal state.")
