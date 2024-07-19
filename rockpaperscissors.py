# Imports
import random
import time
import pygame as pgm
# Settings
players = 999
generations = 100 
delay = 100 # Milliseconds
mutation_rate = 0.01

# Initial distribution
percentage_distribution = {"rock": 33, "paper": 33, "scissors": 33}

# pgm setup
pgm.init()
screen = pgm.display.set_mode((1280, 720))
clock = pgm.time.Clock()
running = True

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
        print(f"Generation {generation + 1}:")
        display(distribution)
        time.sleep(delay/1000)

# Run the simulation
simulate_generations(distribution, generations, delay)
