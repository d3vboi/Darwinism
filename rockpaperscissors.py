import random
import time
import pygame as pgm
import threading

# Settings
players = 999
generations = 1000 
delay = 100  # Milliseconds
mutation_rate = 0.0001

# Initial distribution
percentage_distribution = {"rock": 33, "paper": 33, "scissors": 33}

# Interpret the percentage distribution into actual values
total_percentage = sum(percentage_distribution.values())
players_remaining = players
distribution = {}

# Convert percentages to player counts
for strat in percentage_distribution:
    distribution[strat] = int(players * (percentage_distribution[strat] / total_percentage))
    players_remaining -= distribution[strat]

# Equally distribute any remaining players
strategies = list(distribution.keys())
for i in range(players_remaining):
    distribution[strategies[i % len(strategies)]] += 1

# Shared data structure for synchronization
distribution_lock = threading.Lock()
current_distribution = distribution.copy()

def display(distribution):
    print(f"Total players: {sum(distribution.values())}")
    print("Distribution:")
    for strat in distribution:
        print(f"\t{strat}: {distribution[strat]}")

def play_game(p1, p2):
    # Define rules
    rules = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }
    
    # Check for a tie
    if p1 == p2:
        return ("draw", p1)
    
    # Determine the winner
    if rules[p1] == p2:
        return ("p1", p1)
    else:
        return ("p2", p2)
    
def mutate(strategy):
    strategies = ["rock", "paper", "scissors"]
    strategies.remove(strategy)
    return random.choice(strategies)

def simulate_generations(distribution, generations, delay):
    global current_distribution
    for generation in range(generations):
        new_distribution = {"rock": 0, "paper": 0, "scissors": 0}
        total_players = sum(distribution.values())
        
        # Each player plays a game
        for _ in range(total_players // 2):  # Each pair plays a game
            p1 = random.choices(list(distribution.keys()), list(distribution.values()))[0]
            p2 = random.choices(list(distribution.keys()), list(distribution.values()))[0]
            result, winner = play_game(p1, p2)
            
            if result == "draw":
                # Each player has one child
                child1 = p1 if random.random() > mutation_rate else mutate(p1)
                child2 = p2 if random.random() > mutation_rate else mutate(p2)
                new_distribution[child1] += 1
                new_distribution[child2] += 1
            elif result == "p1":
                # Winner has two children
                child1 = p1 if random.random() > mutation_rate else mutate(p1)
                child2 = p1 if random.random() > mutation_rate else mutate(p1)
                new_distribution[child1] += 1
                new_distribution[child2] += 1
            else:
                # Winner has two children
                child1 = p2 if random.random() > mutation_rate else mutate(p2)
                child2 = p2 if random.random() > mutation_rate else mutate(p2)
                new_distribution[child1] += 1
                new_distribution[child2] += 1
        
        # If there's an odd number of players, one player doesn't get to play
        if total_players % 2 == 1:
            p1 = random.choices(list(distribution.keys()), list(distribution.values()))[0]
            child = p1 if random.random() > mutation_rate else mutate(p1)
            new_distribution[child] += 1
        
        distribution = new_distribution

        with distribution_lock:
            current_distribution = distribution.copy()

        print(f"Generation {generation + 1}:")
        display(distribution)
        time.sleep(delay / 1000)

# Pygame setup
def graphics():
    pgm.init()
    screen = pgm.display.set_mode((1280, 720))
    clock = pgm.time.Clock()
    font = pgm.font.Font(None, 36)  # Reduced font size for better fit
    running = True

    while running:
        # Poll for events
        for event in pgm.event.get():
            if event.type == pgm.QUIT:
                running = False

        # Fill the screen with a color to wipe away anything from the last frame
        screen.fill((0, 0, 0))

        with distribution_lock:
            total_players = sum(current_distribution.values())
            rock_percentage = (current_distribution["rock"] / total_players) * 100
            paper_percentage = (current_distribution["paper"] / total_players) * 100
            scissors_percentage = (current_distribution["scissors"] / total_players) * 100

        # Render text
        rock_text = font.render("Rock", True, (255, 0, 0))
        paper_text = font.render("Paper", True, (0, 255, 0))
        scissors_text = font.render("Scissors", True, (0, 0, 255))

        rock_percent = font.render(f"{rock_percentage:.2f}%", True, (255, 0, 0))
        paper_percent = font.render(f"{paper_percentage:.2f}%", True, (0, 255, 0))
        scissors_percent = font.render(f"{scissors_percentage:.2f}%", True, (0, 0, 255))

        # Calculate bar heights and positions
        max_bar_height = 500
        bar_width = 50
        bar_spacing = 100
        bar_x_start = 100
        bar_y = 500

        # Rock bar
        rock_height = (rock_percentage / 100) * max_bar_height
        rock_bar = pgm.Rect(bar_x_start, bar_y - rock_height, bar_width, rock_height)
        pgm.draw.rect(screen, (255, 0, 0), rock_bar)
        screen.blit(rock_text, (bar_x_start, bar_y + 10))
        screen.blit(rock_percent, (bar_x_start, bar_y + 40))

        # Paper bar
        paper_height = (paper_percentage / 100) * max_bar_height
        paper_bar = pgm.Rect(bar_x_start + bar_spacing, bar_y - paper_height, bar_width, paper_height)
        pgm.draw.rect(screen, (0, 255, 0), paper_bar)
        screen.blit(paper_text, (bar_x_start + bar_spacing, bar_y + 10))
        screen.blit(paper_percent, (bar_x_start + bar_spacing, bar_y + 40))

        # Scissors bar
        scissors_height = (scissors_percentage / 100) * max_bar_height
        scissors_bar = pgm.Rect(bar_x_start + 2 * bar_spacing, bar_y - scissors_height, bar_width, scissors_height)
        pgm.draw.rect(screen, (0, 0, 255), scissors_bar)
        screen.blit(scissors_text, (bar_x_start + 2 * bar_spacing, bar_y + 10))
        screen.blit(scissors_percent, (bar_x_start + 2 * bar_spacing, bar_y + 40))

        pgm.display.flip()

        clock.tick(60)  # Limits FPS to 60

    pgm.quit()

# Run the simulation
simulation_thread = threading.Thread(target=simulate_generations, args=(distribution, generations, delay))
graphics_thread = threading.Thread(target=graphics)

simulation_thread.start()
graphics_thread.start()

simulation_thread.join()
graphics_thread.join()
