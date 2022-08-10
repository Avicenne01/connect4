# Connect 4
![use](https://img.shields.io/badge/use-Project-green) 

[Connect 4](https://en.wikipedia.org/wiki/Connect_Four) game implemented in python.

## Setup

1. Clone this git repository:
   - Open your terminal and move to a directory of your choice using `cd` command.
   - Run
   ```bash
   $ git clone https://github.com/chrichri17/connect4.git
   ```
   - Run `cd connect4`
2. Create a virtual environment
   ```bash
   $ python3 -m venv venv
   ```
3. Activate your virtual environment
   - for unix users:
   ```bash
   $ source venv/bin/activate
   ```
   - for windows users:
   ```bash
   $ source venv/Scripts/activate
   ```
4. Install the necessary python dependencies for this project
   ```bash
   $ pip3 install -r requirements.dev.txt
   ```

## How to play ?

Connect4 can be played by 3 different players:

- `HumanPlayer`: you or your friends
- `RandomPlayer`: a player that drop token randomly
- `AIPlayer`: a more intelligent player who thinks about strategy and can even beat a human. It depends on how you implement it though. There is a lot of strategy one can choose. In this project we will use the [Alpha-Beta pruning algorithm](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning "{isExternal}"). [Reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning "{isExternal}") is another strategy we might want to try.

Right now, players are set up in the code. To do so, open [`connect4/main.py`](main.py) and update the body as follow:

```python
if __name__ == "__main__":
   player1 = AlphaBetaPlayer("I'm gonna beat you")
   player2 = HumanPlayer("John Snow")

   # Snipp...
```

Then open your terminal and run `$ python3 main.py` (assuming your are in the directory `connect4/`).

## Documentation
Please refer to [Docs.md](./Docs.md)

## Author
[Merchrist KIKI](mailto:alexismerchrist.kiki@gmail.com)

## Contributors
- [DEGNI Fidèle](mailto:defidele@gmail.com)
- [ADAM Bassimath](mailto:bassimath@gmail.com)