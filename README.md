# Soccer Manager Game

A terminal-based soccer management simulation game where you can manage both a senior team and its youth academy. Experience detailed match simulations with personality-driven player actions and comprehensive team management features.

## Features

- **Team & Player Management**
  - Manage both senior team and youth academy
  - Players with unique personalities affecting their play style
  - Detailed player attributes and statistics
  - Youth player development and promotion system

- **Match Simulation**
  - Detailed, real-time match commentary
  - Personality-driven player decisions
  - Comprehensive match statistics
  - Dynamic player interactions based on attributes and personalities

- **League System**
  - Multiple professional leagues (English, Spanish, German)
  - Full season fixture generation
  - League standings and statistics
  - Week-by-week simulation

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd soccer-manager
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## How to Play

1. Start the game:
```bash
python game.py
```

2. Select a league and team to manage

3. Use the main menu to:
   - View and manage your squad
   - Check your youth academy
   - View league standings
   - Play matches
   - Promote youth players
   - And more!

## Game Mechanics

### Player Personalities

Players have one of three personalities that affect their attributes and in-game decisions:

1. **Maverick**
   - Increases: dribbling, finishing, dribbling skills
   - Decreases: playmaking, passing, long balls
   - More likely to: dribble, call for ball, shoot
   - Less likely to: pass, play long balls

2. **Heartbeat**
   - Increases: playmaking, passing, long balls
   - Decreases: dribbling, dribbling skills, finishing
   - More likely to: pass, play long balls
   - Less likely to: call for ball, shoot, dribble

3. **Vitroso**
   - Increases: dribbling, passing, accuracy
   - Decreases: dribbling skills, long balls
   - More likely to: call for ball, make runs, pass
   - Less likely to: play long balls

### Match Simulation

Matches are simulated with detailed commentary showing:
- Who has possession
- Player actions and decisions
- Success/failure of actions
- Goals and key events
- Match statistics

### Youth Academy

- Each team has a youth academy
- Youth players can be promoted when they reach certain rating thresholds
- Watch youth matches to scout emerging talent
- Develop young players through training and matches

## Contributing

Feel free to submit issues and enhancement requests! 