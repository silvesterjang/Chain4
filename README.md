---<br>
<br>
title: Chain 4<br>
description: A game for 'ESCamp-2012 AI Competition'<br>
author: Jaehyun Jang<br>
tags: pygame, game, python<br>
created:  2013 Jan 13<br>
modified: 2013 Jan 31<br>
---<br>

Chain 4
=========

This game has one objective which player can put one block or 2 block (if player use chance, each player has 2 chances.) his / her turn.
If player select a row which he or she want to place, the block is placed at closest to wall with empty place. <br>

(e.g OOOXXXX - row 2, O is not empty, X is empty. <br>
													if player select put(2) <br>
	OOOOXXX - row 2, O is not empty, X is empty. <br>
)

if player make 4 blocks chained horizontally, vertically, or diagonally, that player wins.

Pygame is main module for running this game. if you did not install it, please visit "http://www.pygame.org/news.html" site and intall appropriate your os with python version.

This source code consists of server - client using socket. If you want to make own client, please refer original python source code.

How to run?
=========
1. server -> python server.py (port number)
2. client -> client.py (address port number), if you edit your own heuristic, please edit 'ai.py' code.
