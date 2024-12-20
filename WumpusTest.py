import sys
from collections import deque

class Block:
    def __init__(self, visited, maybeWumpus, maybePit, maybeGold, gold, breeze, smell, glitter):
        self.visited = visited
        self.maybeWumpus = maybeWumpus
        self.maybePit = maybePit
        self.maybeGold = maybeGold
        self.gold = gold
        self.breeze = breeze
        self.smell = smell
        self.glitter = glitter

def setDangers(board, curX, curY):
    rows = len(board)
    cols = len(board[0])
    
    if board[curY][curX].visited:
        board[curY][curX].maybeWumpus = False
        board[curY][curX].maybePit = False
        board[curY][curX].maybeGold = False
        return
    if board[curY][curX].maybeWumpus:
        # Check if any surrounding block is visited and not smelly
        if curY - 1 >= 0 and board[curY - 1][curX].visited:
            if not board[curY - 1][curX].smell:
                board[curY][curX].maybeWumpus = False
        if curY + 1 < rows and board[curY + 1][curX].visited:
            if not board[curY + 1][curX].smell:
                board[curY][curX].maybeWumpus = False
        if curX - 1 >= 0 and board[curY][curX - 1].visited:
            if not board[curY][curX - 1].smell:
                board[curY][curX].maybeWumpus = False
        if curX + 1 < cols and board[curY][curX + 1].visited:
            if not board[curY][curX + 1].smell:
                board[curY][curX].maybeWumpus = False
    if board[curY][curX].maybePit:
        # Check if any surrounding block is visited and not breezy
        if curY - 1 >= 0 and board[curY - 1][curX].visited:
            if not board[curY - 1][curX].breeze:
                board[curY][curX].maybePit = False
        if curY + 1 < rows and board[curY + 1][curX].visited:
            if not board[curY + 1][curX].breeze:
                board[curY][curX].maybePit = False
        if curX - 1 >= 0 and board[curY][curX - 1].visited:
            if not board[curY][curX - 1].breeze:
                board[curY][curX].maybePit = False
        if curX + 1 < cols and board[curY][curX + 1].visited:
            if not board[curY][curX + 1].breeze:
                board[curY][curX].maybePit = False
    if board[curY][curX].maybeGold:
        # Check if any surrounding block is visited and not glitter
        if curY - 1 >= 0 and board[curY - 1][curX].visited:
            if not board[curY - 1][curX].glitter:
                board[curY][curX].gold = False
                board[curY][curX].maybeGold = False
        if curY + 1 < rows and board[curY + 1][curX].visited:
            if not board[curY + 1][curX].glitter:
                board[curY][curX].gold = False
                board[curY][curX].maybeGold = False
        if curX - 1 >= 0 and board[curY][curX - 1].visited:
            if not board[curY][curX - 1].glitter:
                board[curY][curX].gold = False
                board[curY][curX].maybeGold = False
        if curX + 1 < cols and board[curY][curX + 1].visited:
            if not board[curY][curX + 1].glitter:
                board[curY][curX].gold = False
                board[curY][curX].maybeGold = False

def get_environment_input():
    # Request input from the test harness
    sys.stdout.write("input:\n")
    sys.stdout.flush()
    
    # Read the numerical result from the test harness
    input_data = sys.stdin.readline().strip()
    return int(input_data)

def processInput(board, inputValue, curX, curY):
    rows = len(board)
    cols = len(board[0])
    
    while inputValue > 0:
        if inputValue >= 8:
            # found gold
            board[curY][curX].gold = True
            inputValue -= 8
        elif inputValue >= 4:
            # glitter
            board[curY][curX].glitter = True
            # Set surrounding places
            if curY - 1 >= 0 and not board[curY - 1][curX].visited:
                board[curY - 1][curX].maybeGold = True
            if curY + 1 < rows and not board[curY + 1][curX].visited:
                board[curY + 1][curX].maybeGold = True
            if curX - 1 >= 0 and not board[curY][curX - 1].visited:
                board[curY][curX - 1].maybeGold = True
            if curX + 1 < cols and not board[curY][curX + 1].visited:
                board[curY][curX + 1].maybeGold = True
            inputValue -= 4
        elif inputValue >= 2:
            # smelly
            board[curY][curX].smell = True
            # Set surrounding places
            if curY - 1 >= 0 and not board[curY - 1][curX].visited:
                board[curY - 1][curX].maybeWumpus = True
            if curY + 1 < rows and not board[curY + 1][curX].visited:
                board[curY + 1][curX].maybeWumpus = True
            if curX - 1 >= 0 and not board[curY][curX - 1].visited:
                board[curY][curX - 1].maybeWumpus = True
            if curX + 1 < cols and not board[curY][curX + 1].visited:
                board[curY][curX + 1].maybeWumpus = True
            inputValue -= 2
        elif inputValue >= 1:
            # breezy
            board[curY][curX].breeze = True
            # Set surrounding places
            if curY - 1 >= 0 and not board[curY - 1][curX].visited:
                board[curY - 1][curX].maybePit = True
            if curY + 1 < rows and not board[curY + 1][curX].visited:
                board[curY + 1][curX].maybePit = True
            if curX - 1 >= 0 and not board[curY][curX - 1].visited:
                board[curY][curX - 1].maybePit = True
            if curX + 1 < cols and not board[curY][curX + 1].visited:
                board[curY][curX + 1].maybePit = True
            inputValue -= 1
        else:
            # Should not happen
            break

def isSafe(board, curX, curY):
    return not board[curY][curX].maybeWumpus and not board[curY][curX].maybePit

def pathFind(board, path, curX, curY):
    rows = len(board)
    cols = len(board[0])

    # First, try to find a safe, unvisited, maybeGold block
    queue = deque()
    visited_positions = set()

    # Enqueue starting position
    queue.append((curX, curY, []))
    visited_positions.add((curX, curY))

    while queue:
        x, y, path_so_far = queue.popleft()

        # Check if this is a safe, unvisited, maybeGold block
        if not board[y][x].visited and isSafe(board, x, y) and board[y][x].maybeGold:
            # Found our target
            path.extend(path_so_far + [(x, y)])
            return

        # Enqueue neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if (nx, ny) not in visited_positions and isSafe(board, nx, ny):
                    visited_positions.add((nx, ny))
                    queue.append((nx, ny, path_so_far + [(x, y)]))

    # If no safe, maybeGold block found, find any safe, unvisited block
    queue = deque()
    visited_positions = set()
    queue.append((curX, curY, []))
    visited_positions.add((curX, curY))

    while queue:
        x, y, path_so_far = queue.popleft()

        # Check if this is a safe, unvisited block
        if not board[y][x].visited and isSafe(board, x, y):
            # Found our target
            path.extend(path_so_far + [(x, y)])
            return

        # Enqueue neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if (nx, ny) not in visited_positions and isSafe(board, nx, ny):
                    visited_positions.add((nx, ny))
                    queue.append((nx, ny, path_so_far + [(x, y)]))

    # If no safe, unvisited block found, clear the path
    path.clear()

def pathFindToStart(board, path, curX, curY):
    rows = len(board)
    cols = len(board[0])

    # Find path back to (0, 0)
    queue = deque()
    visited_positions = set()

    # Enqueue starting position
    queue.append((curX, curY, []))
    visited_positions.add((curX, curY))

    while queue:
        x, y, path_so_far = queue.popleft()

        # Check if this is the starting block
        if x == 0 and y == 0:
            # Found our target
            path.extend(path_so_far + [(x, y)])
            return

        # Enqueue neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if (nx, ny) not in visited_positions and isSafe(board, nx, ny):
                    visited_positions.add((nx, ny))
                    queue.append((nx, ny, path_so_far + [(x, y)]))

    # If no path found, clear the path
    path.clear()

def main():
    curX = 0
    curY = 0
    board = [[Block(False, False, False, False, False, False, False, False) for _ in range(4)] for _ in range(4)]

    hasPath = False
    path = []

    hasGold = False  # Flag to indicate if gold has been found

    while True:
        # If the current block hasn't been visited
        if not board[curY][curX].visited:
            # Get input from the environment
            inputValue = get_environment_input()
            processInput(board, inputValue, curX, curY)

            # Mark the block as visited
            board[curY][curX].visited = True

            # Check if gold is found
            if board[curY][curX].gold:
                hasGold = True
                # Find path back to start
                path.clear()
                pathFindToStart(board, path, curX, curY)
                hasPath = True
                continue  # Proceed to move back to start

            # Recalculate dangers
            for y in range(4):
                for x in range(4):
                    setDangers(board, x, y)

        # Determine next action
        if not hasPath:
            hasPath = True
            path.clear()
            pathFind(board, path, curX, curY)
            if not path:
                # No safe path found
                sys.stderr.write("No safe path found.\n")
                sys.stderr.flush()
                break

        # Move to next position in path
        nextX, nextY = path.pop(0)
        if nextX > curX:
            action = "e"
        elif nextX < curX:
            action = "w"
        elif nextY > curY:
            action = "n"
        elif nextY < curY:
            action = "s"
        else:
            action = ""

        if action:
            sys.stdout.write(action + "\n")
            sys.stdout.flush()
            curX, curY = nextX, nextY
        else:
            # No movement needed
            pass

        # Reset hasPath if path is exhausted
        if not path:
            hasPath = False

        # Check if back at starting position with gold
        if hasGold and curX == 0 and curY == 0:
            break  # Exit the loop and end the program

if __name__ == "__main__":
    main()