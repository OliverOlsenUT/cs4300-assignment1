import copy
class BFSNode():
    def __init__(self):
        self.left_river = set()
        self.right_river = set()
        self.prev_actions = []
    def __eq__(self, other):
        other : BFSNode
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
        return str(self.left_river) + ", " + str(self.right_river) + ", " + str(self.prev_actions)
class BFS():
    def __init__(self):
        self.queue = []
        self.goal = BFSNode()
        self.goal.right_river.add("farmer")
        self.goal.right_river.add("goat")
        self.goal.right_river.add("cabbage")
        self.goal.right_river.add("wolf")
        self.explored = set()
    def ENQUEUE(self, item):
        self.queue.append(item)
    def DEQUEUE(self):
        return self.queue.pop()
    def GOAL_TEST(self, n):
        return n == self.goal
    def TRANSITION(self, n, a):
        n_ = copy.deepcopy(n)
        n_ : BFSNode
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
    def MAIN(self, s0):
        self.queue = []
        self.ENQUEUE(s0)
        self.explored = []
        while self.queue:
            n = self.DEQUEUE()
            if self.GOAL_TEST(n):
                return n
            self.explored.append(n)
            for a in n.actions():
                s_ = self.TRANSITION(n, a)
                if s_ not in self.queue and s_ not in self.explored:
                    self.ENQUEUE(s_)
        return "fail"

if __name__ == "__main__":
    b = BFS()
    s0 = BFSNode()
    s0.left_river.add("farmer")
    s0.left_river.add("goat")
    s0.left_river.add("cabbage")
    s0.left_river.add("wolf")
    print(b.MAIN(s0)) 
    s0 = BFSNode()
    s0.right_river.add("farmer")
    s0.right_river.add("goat")
    s0.left_river.add("cabbage")
    s0.left_river.add("wolf")
    print(b.MAIN(s0)) 