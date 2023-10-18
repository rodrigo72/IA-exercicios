from Grafo import Graph
from collections import deque


class Bucket:

    def __init__(self, start="(0,0)", goal="(2,0)", cap1=4, cap2=3):
        self.g = Graph(directed=True)
        self.start = start
        self.goal = goal
        self.bucket_1 = cap1
        self.bucket_2 = cap2

    def get_states(self, bucket1, bucket2):
        return [
            (self.bucket_1, bucket2),  # fill bucket 1
            (bucket1, self.bucket_2),  # fill bucket 2
            (0, bucket2),  # empty bucket 1
            (bucket1, 0),  # empty bucket 2
            # first bucket cannot overflow, and second bucket will be with the remaining water
            (min(bucket1 + bucket2, self.bucket_1), max(0, bucket1 + bucket2 - self.bucket_1)),  # transfer 2 to 1
            (max(0, bucket1 + bucket2 - self.bucket_2), min(bucket1 + bucket2, self.bucket_2))   # transfer 1 to 2
        ]

    def solve_with_bfs(self):
        initial_state = self.start
        queue = deque([initial_state])
        visited = {initial_state: None}

        while queue:
            current_state = queue.popleft()

            if current_state == self.goal:
                path = []
                while current_state:
                    path.append(current_state)
                    current_state = visited[current_state]
                return path[::-1]

            bucket1 = int(current_state[1])
            bucket2 = int(current_state[3])

            new_states = self.get_states(bucket1, bucket2)

            for new_state in new_states:
                new_state_str = "(" + str(new_state[0]) + "," + str(new_state[1]) + ")"
                if new_state_str not in visited:
                    visited[new_state_str] = current_state
                    queue.append(new_state_str)

        return None  # if no solution found

    def solve_with_dfs(self, start=None, visited=None, path=None):
        if visited is None:
            visited = set()

        if start is None:
            start = self.start

        if path is None:
            path = []

        visited.add(start)
        path.append(start)

        if start == self.goal:
            return path

        bucket1 = int(start[1])
        bucket2 = int(start[3])

        new_states = self.get_states(bucket1, bucket2)

        for new_state in new_states:
            new_state_str = "(" + str(new_state[0]) + "," + str(new_state[1]) + ")"
            if new_state_str not in visited:
                result = self.solve_with_dfs(new_state_str, visited, path)
                if result is not None:
                    return result

        path.pop()
        return None

