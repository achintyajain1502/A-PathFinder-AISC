import tkinter as tk
import heapq

# -----------------------------
# Settings
# -----------------------------

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 650

ROWS = 20
COLS = 25
CELL_SIZE = 25

# -----------------------------
# Variables
# -----------------------------

start = None
goal = None

obstacles = set()

path = []

visited = set()

searching = False

# -----------------------------
# Create Window
# -----------------------------

window = tk.Tk()

window.title("A* Pathfinding Visualizer")

window.geometry(
    f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
)

# -----------------------------
# Title
# -----------------------------

title = tk.Label(
    window,
    text="A* Pathfinding Visualizer",
    font=("Arial", 20, "bold")
)

title.pack(pady=10)


instructions = tk.Label(
    window,
    text="First click = Start | Second click = Goal | Other clicks = Obstacles",
    font=("Arial", 10)
)

instructions.pack(pady=5)

# -----------------------------
# Canvas
# -----------------------------

canvas = tk.Canvas(
    window,
    width=COLS * CELL_SIZE,
    height=ROWS * CELL_SIZE,
    bg="white"
)

canvas.pack()


# -----------------------------
# Create Grid
# -----------------------------

def create_grid():

    canvas.delete("all")

    for row in range(ROWS):

        for col in range(COLS):

            cell = (row, col)

            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE

            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            # Start
            if cell == start:

                color = "green"

            # Goal
            elif cell == goal:

                color = "red"

            # Obstacles
            elif cell in obstacles:

                color = "black"

            # Final path
            elif cell in path:

                color = "yellow"

            # Visited/search nodes
            elif cell in visited:

                color = "orange"

            # Empty cell
            else:

                color = "white"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="gray"
            )


# -----------------------------
# Mouse Click
# -----------------------------

def cell_clicked(event):

    global start, goal

    # Don't allow clicking during search
    if searching:
        return

    row = event.y // CELL_SIZE
    col = event.x // CELL_SIZE

    if row >= ROWS or col >= COLS:
        return

    cell = (row, col)

    # First click = Start
    if start is None:

        start = cell

    # Second click = Goal
    elif goal is None and cell != start:

        goal = cell

    # Other clicks = Obstacles
    elif cell != start and cell != goal:

        if cell in obstacles:

            obstacles.remove(cell)

        else:

            obstacles.add(cell)

    create_grid()


# -----------------------------
# Manhattan Distance
# -----------------------------

def heuristic(node, goal_node):

    return (
        abs(node[0] - goal_node[0])
        + abs(node[1] - goal_node[1])
    )


# -----------------------------
# Get Neighbors
# -----------------------------

def get_neighbors(node):

    row, col = node

    neighbors = [

        (row - 1, col),

        (row + 1, col),

        (row, col - 1),

        (row, col + 1)

    ]

    valid_neighbors = []

    for neighbor in neighbors:

        r, c = neighbor

        if (

            0 <= r < ROWS

            and 0 <= c < COLS

            and neighbor not in obstacles

        ):

            valid_neighbors.append(neighbor)

    return valid_neighbors


# -----------------------------
# A* Search Animation
# -----------------------------

def astar():

    global path
    global visited
    global searching

    # Priority queue
    open_list = []

    heapq.heappush(
        open_list,
        (0, start)
    )

    # Previous node
    came_from = {}

    # Cost from start
    g_score = {}

    for row in range(ROWS):

        for col in range(COLS):

            g_score[(row, col)] = float("inf")

    g_score[start] = 0

    visited.clear()

    searching = True

    search_step(
        open_list,
        came_from,
        g_score
    )


# -----------------------------
# Search Step
# -----------------------------

def search_step(
    open_list,
    came_from,
    g_score
):

    global path
    global searching

    # No nodes left
    if not open_list:

        searching = False

        status_label.config(
            text="No path exists!"
        )

        return

    # Get lowest f-score node
    current_f, current = heapq.heappop(
        open_list
    )

    # Goal reached
    if current == goal:

        path = []

        while current in came_from:

            path.append(current)

            current = came_from[current]

        path.append(start)

        path.reverse()

        searching = False

        status_label.config(
            text=f"Path found! Length: {len(path) - 1}"
        )

        create_grid()

        return

    # Add current node to visited
    visited.add(current)

    # Explore neighbors
    for neighbor in get_neighbors(current):

        tentative_g = (
            g_score[current] + 1
        )

        if tentative_g < g_score[neighbor]:

            came_from[neighbor] = current

            g_score[neighbor] = tentative_g

            h_score = heuristic(
                neighbor,
                goal
            )

            f_score = (
                tentative_g + h_score
            )

            heapq.heappush(
                open_list,
                (f_score, neighbor)
            )

    # Update screen
    create_grid()

    # Continue search after 100 milliseconds
    window.after(
        800,
        lambda: search_step(
            open_list,
            came_from,
            g_score
        )
    )


# -----------------------------
# Start A*
# -----------------------------

def start_astar():

    global path

    if start is None or goal is None:

        status_label.config(
            text="Please select Start and Goal first."
        )

        return

    if start in obstacles or goal in obstacles:

        status_label.config(
            text="Start or Goal cannot be an obstacle."
        )

        return

    path = []

    status_label.config(
        text="A* is searching..."
    )

    astar()


# -----------------------------
# Reset
# -----------------------------

def reset_grid():

    global start
    global goal
    global path
    global visited
    global searching

    start = None

    goal = None

    path = []

    visited = set()

    searching = False

    obstacles.clear()

    status_label.config(
        text="Select Start and Goal"
    )

    create_grid()


# -----------------------------
# Buttons
# -----------------------------

button_frame = tk.Frame(window)

button_frame.pack(pady=10)


start_button = tk.Button(
    button_frame,
    text="Start A*",
    font=("Arial", 12, "bold"),
    command=start_astar
)

start_button.pack(
    side=tk.LEFT,
    padx=10
)


reset_button = tk.Button(
    button_frame,
    text="Reset",
    font=("Arial", 12),
    command=reset_grid
)

reset_button.pack(
    side=tk.LEFT,
    padx=10
)


# -----------------------------
# Status
# -----------------------------

status_label = tk.Label(
    window,
    text="Select Start and Goal",
    font=("Arial", 11)
)

status_label.pack(pady=5)


# -----------------------------
# Mouse Binding
# -----------------------------

canvas.bind(
    "<Button-1>",
    cell_clicked
)


# -----------------------------
# Initial Grid
# -----------------------------

create_grid()


# -----------------------------
# Run Application
# -----------------------------

window.mainloop()