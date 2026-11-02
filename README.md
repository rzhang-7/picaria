# Picaria Game w/ UDP Connection

Created by: **Raymond Zhang** and **Lev Shlyonsky**

Emulates a game of Picaria using python. Picaria is a two player Indigenous American game from Southwestern USA. It is very similar to TicTacToe in that both players try to align three tiles in a row. However, each player may place down three tiles only and each subsequent turn will involve a player moving one of their tiles to an adjacent spot on the grid.

## Features ✨

Notable features of this particular edition include:

- Clean GUI made with the Pygame library
- Audio cues
- Menu screen
- Rules page
- Option to play again
- Wireless connection between players via UDP

## Installation and Use 📝

### Before Installation

Prior to installation, please ensure that players have the (preferably) latest versions of [Python](https://www.python.org/) and [Pygame](https://www.pygame.org/) installed on both of their devices. Download instructions of both can be found on their respective websites.

### Installation

In the package there is an assets folder, a file named `Player 1.py` and another named `Player 2.py`. Both players must download the assets folder and their respective files. Note that Player 1 will always go first as black and Player 2 will always go second as white.

### Use

In order to play with another device, you need to find the IP address of both Player 1 and Player 2's devices.

Then, you must use a text editor to manually enter the IP addresses into the programs. As mentioned in the program comments, the player should put the IP of their own device in the quotations of `MY_IP` and their opponent's IP in the quotations of `RCV_IP`.

Afterwards, both players can run their Python programs through their command line or using an IDE.
