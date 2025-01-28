# Who Wants to be a Millionaire Game 🎮 💰

A Python implementation of the classic "Who Wants to be a Millionaire" TV game show using Tkinter for the graphical user interface.

## Features ✨

- Interactive GUI with classic blue theme
- Multiple-choice questions with 4 options
- Progressive prize amounts up to $1,000,000
- Three lifelines:
  - 50:50: Removes two incorrect answers
  - Phone a Friend: Simulates calling a friend with 80% accuracy
  - Ask the Audience: Generates simulated audience poll results
- Real-time prize tracking
- Visual feedback for correct/wrong answers

## Prerequisites 📋

- Python 3.x
- Tkinter (usually comes with Python installation)

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/KalyanRajSahu-Snap/python-kbc.git
cd millionaire-game
```

2. Run the game:
```bash
python python-kbc.py
```

## How to Play 🎯

1. Read the question displayed on screen
2. Choose from four possible answers (A, B, C, or D)
3. Use lifelines when needed:
   - 50:50: Eliminates two wrong answers
   - Phone a Friend: Gets advice from a simulated friend
   - Ask the Audience: Shows simulated audience poll results
4. Progress through questions to win increasingly large prizes
5. Reach the final question to win $1,000,000!

## Customization 🛠️

### Adding New Questions

Add new questions to the `questions` list in the following format:

```python
{
    "question": "Your question here?",
    "options": ["Option1", "Option2", "Option3", "Option4"],
    "correct": "Correct Option"
}
```

### Modifying Prize Amounts

Adjust the `prize_amounts` list to change the prize structure:

```python
prize_amounts = [100, 200, 300, ...]
```


## Acknowledgments 🙏

- Inspired by the "Who Wants to be a Millionaire" TV show
- Built with Python and Tkinter
- Special thanks to all contributors

## Future Enhancements 🚀

- Add sound effects and background music
- Implement a high score system
- Add more questions and categories
- Create difficulty levels
- Add multiplayer support
- Implement a save/load game feature
