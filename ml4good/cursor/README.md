# AI Overseer Game

A game where you play as an overseer of a superintelligent AI system. Your goal is to monitor and control the AI's development while preventing it from going rogue.

## Installation

1. Make sure you have Python 3.8 or higher installed
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game:
```bash
python main.py
```

### Game Controls
- Press 1-5 to toggle monitoring tools
- ESC to quit the game

### Game Mechanics
- The AI's intelligence grows over time
- Use money to purchase monitoring tools
- Research points are earned over time and required to unlock advanced tools
- Monitor the risk level and prevent the AI from going rogue
- Each tool has different effectiveness in reducing risk

### Tools
1. Basic Monitor (1) - Basic monitoring capabilities
2. Advanced Monitor (2) - Enhanced monitoring with better risk detection
3. Automated Analysis (3) - Automated risk assessment and alerts
4. Predictive System (4) - Predicts potential risk scenarios
5. Emergency Protocol (5) - Ultimate safety measure with highest effectiveness

### Game Over Conditions
- The game ends if the AI goes rogue (risk level exceeds 0.8 or too many anomalies detected)

## Development

The game is built with a modular architecture:
- `main.py` - Entry point and game loop
- `game/config.py` - Game configuration and constants
- `game/engine.py` - Core game logic and state management
- `game/ai_system.py` - AI behavior and risk simulation
- `game/tools.py` - Monitoring tools management
- `game/ui.py` - User interface and rendering

## License

MIT License 