# Tic Tac Toe Reinforcement Learning
## Introduction

This repository contains the implementation of a Tic Tac Toe game using Reinforcement Learning. In contrast to traditional game theory methods like the min-max algorithm, this approach does not assume a perfect opponent but leverages Reinforcement Learning to interact with the environment, resulting in a more adaptive and flexible strategy.

## Project Overview

This project focuses on training two agents to play against each other and then allowing the trained agent to play against a human player. The core components of the project include:

1. State Setting: A State class that represents the game board and handles the state, action, and reward components of the Reinforcement Learning problem.

2. Player Setting: A Player class that represents the agent, allowing it to choose actions, record game states, update state-value estimations, and save/load its policy.

3. Training: The process where two agents play against each other, selecting available positions, updating the board state, and assigning rewards based on game outcomes.

4. Saving & Loading Policy: Storing the learned policy after training to enable the agent to play against a human player.

5. Human VS Computer: A class that allows a human player to play against the trained agent.

## State Setting

The State class serves as the game board and judger, managing the board state, actions, and rewards. The key components include:

* Board State: A 3x3 board representing the positions of both players.
* Action: Legal positions a player can choose.
* Reward: A value between 0 and 1 given at the end of the game.

## Player Setting

The Player class represents the agent and provides functionalities for:

* Choosing Actions: Balancing exploration and exploitation using an ε-greedy method.
* Recording Game States: Keeping track of positions taken during each game.
* Updating State-Value Estimations: Using value iteration to update estimations based on observed rewards.
* Saving & Loading Policy: Storing and retrieving the learned policy.

## Training

During training, two agents interact, selecting available positions, updating the board state, and assigning rewards based on game outcomes. The training process enables the agent to improve its policy over time.

## Saving & Loading Policy

At the end of training, the agent's policy, stored in the state-value dictionary, can be saved for later use, allowing the agent to play against a human player.

## Human VS Computer

A Human class is included to facilitate human-player interaction with the trained agent. The play function displays the board state and accepts the human player's input.

## Getting Started

To start playing Tic Tac Toe against the trained agent, follow these steps:

1. Clone this repository.
2. Run the tic_tac_toe.py script.
3. Follow the on-screen instructions to play against the agent.

## Conclusion

This project demonstrates the application of Reinforcement Learning to train agents to play Tic Tac Toe. By considering the opponent as part of the environment, the agents can learn to make strategic moves without presuming a model of the opponent. We hope you enjoy playing the game and exploring the capabilities of Reinforcement Learning in game strategy development.

# License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/nikitgoku/rl_implementation/blob/main/LICENSE/ "LICENCE title") file for details.

Acknowledgments

* Inspired by Reinforcement Learning principles.
* Built using Python.
