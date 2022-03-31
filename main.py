import pygame
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (255, 100, 0)

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH+1, HEIGHT + 80))

clock = pygame.time.Clock()

font = pygame.font.SysFont("bell", 28)

class Node:
        def __init__(self, x, y, node_side):
            self.x, self.y = x, y
            self.neighbours = []
            self.obstacle = False
            self.parent = None
            self.visited = False
            self.node_side = node_side
            self.color = BLACK
            self.path_part = False

        def draw(self, screen):
            if self.visited and  not self.path_part :
                self.color = YELLOW
            pygame.draw.rect(screen, self.color, (self.x * self.node_side + 1, self.y * self.node_side + 1, self.node_side-1, self.node_side-1))
        
# Adding adjacent nodes as neighbours
def add_neigh(grid, rows, cols):
    for i in range(rows):
        for j in range(cols):
            # Add neighbours only if node isn't an obstacle
            if not grid[i][j].obstacle:
                if i > 0:
                    grid[i][j].neighbours.append(grid[i - 1][j])
                if i < rows - 1:
                    grid[i][j].neighbours.append(grid[i + 1][j])
                if j < cols - 1:
                    grid[i][j].neighbours.append(grid[i][j + 1])
                if j > 0:
                    grid[i][j].neighbours.append(grid[i][j - 1])

def bfs(screen, start_node, end_node):
    path = []
    queue = []
    queue.append(start_node)

    while(queue):
        # Setting FPS to 240 to get a better visualization
        clock.tick(240)
        curr_node = queue[0]

        # Path has been found
        if curr_node == end_node:
            curr_node.visited = True
            while(curr_node.parent):
                curr_node.path_part = True
                path.append(curr_node)
                curr_node = curr_node.parent
            break
        
        queue.pop(0)
        curr_node.visited = True

        for n in curr_node.neighbours:
            if not n.obstacle:
                if not n.visited:
                    queue.append(n)
                    n.visited = True
                    n.parent = curr_node
        
        curr_node.draw(screen)
        pygame.display.update()
    
    for node in path:
        node.color = BLUE
        node.draw(screen)
        pygame.display.update()

def main():
    # Instruction to be displayed
    messages = [
        "Press Enter after you're done drawing obstacles",
        "Select the starting point",
        "Select the ending point",
        "Press Enter to start BFS",
        "Finding the optimal path...",
        "Optimal Path found! Press Enter to Reset"
    ]
    # Index of instruction/msg
    msg_index = 0

    # Creating the graph/grid
    rows, cols = 30, 30
    # Length of side of each square node
    node_side = 600 // rows
    grid = [[Node(i, j, node_side) for j in range(cols)] for i in range(rows)]
    
    add_neigh(grid, rows, cols)

    screen.fill(BLACK)
    running = True
    drawing_obstacles = False
    drawing_start = False
    drawing_end = False
    start_node = None
    end_node = None

    while(running):
        screen.fill(BLACK)
        # Drawing the actual grid
        for i in range(rows + 1):
            pygame.draw.line(screen, GREY, (i * node_side, 0), (i * node_side, HEIGHT), 1) # Columns
            pygame.draw.line(screen, GREY, (0, i * node_side), (WIDTH, i * node_side), 1) # Rows           

        for event in pygame.event.get():
            # Close window
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Determine action depending on the instruction being displayed
                if msg_index == 0:
                    drawing_obstacles = True
                elif msg_index == 1:
                    drawing_start = True
                elif msg_index == 2:
                    drawing_end = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing_obstacles = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Done drawing obstacles now next instruction
                    if msg_index == 0:
                        msg_index = msg_index + 1
                    elif msg_index == 3:
                        msg_index += 1
                    elif msg_index == 5:
                        main()
        
        if drawing_obstacles:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_x // node_side, mouse_y // node_side # Converting mouse pos to indices of graph
            grid[mouse_x][mouse_y].obstacle = True
            grid[mouse_x][mouse_y].color = GREY

        if drawing_start:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_x // node_side, mouse_y // node_side # Converting mouse pos to indices of graph
            # Starting node will be colored red
            grid[mouse_x][mouse_y].color = RED
            start_node = grid[mouse_x][mouse_y]
            drawing_start = False
            msg_index += 1

        if drawing_end:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_x // node_side, mouse_y // node_side # Converting mouse pos to indices of graph
            # Ending node will be colored green
            grid[mouse_x][mouse_y].color = GREEN
            end_node = grid[mouse_x][mouse_y]
            drawing_end = False
            msg_index += 1

        # Display the instruction
        instruction = font.render(messages[msg_index], True, WHITE)
        screen.blit(instruction, (20, 620)) 

        for i in range(rows):
            for j in range(cols):
                grid[i][j].draw(screen)
        pygame.display.update()

        if msg_index == 4:
            bfs(screen, start_node, end_node)
            msg_index += 1

    return

main()