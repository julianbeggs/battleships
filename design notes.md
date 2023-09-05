initialize game
- create new grid
- create new ships
- set random positions for the ships

player_turn
- get player input: guessed coordinate
- check if guess is hit or miss
    - if hit check if hit and sunk
    - update hit/miss indicators
- update player progress
    - if 5 ships sunk, player wins
