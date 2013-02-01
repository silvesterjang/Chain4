#!/usr/bin/env python
import socket, sys, gc, time
from gamescene import Gamescene
from ai import AI

class Client(object):
	def __init__(self):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self, host, port):
		self.conn.connect((host, port))
		info = self.conn.recv(1024)
		row, col, player = info.split(" ")
		print "-------------Status------------"
		print "WORLD_ROWS : %s" %(row)
		print "WORLD_COLS : %s" %(col)
		print "PLAYER	  : %s" %(player)
		print "-------------------------------\n\n"
		print "Connected. Waiting..."
		if int(player) == 1: print "You are RED."
		else:               print "You are BLUE."

		self.ai = AI(int(row), int(col), int(player))
		self.conn.send(self.ai.name+"\n")
		
		data = self.conn.recv(1024)
		print "Teamname:", self.ai.name
		print "Opponent:", data.strip()
		
	def play(self, viewflag=False) :
		if viewflag == True:
			gamescene = Gamescene(self.ai)
		while True:
			recvdata = self.conn.recv(4096)
			if recvdata in ["WIN\n", "DRAW\n", "LOSE\n"]: 
				print "Result:", recvdata				
				break
			recvdata = recvdata.strip().split(" ")
			self.ai.update(recvdata[1])
			print "*" * 20
			print "ai.map update : "
			print self.ai.map
			print "*" * 20
			response = self.ai.think()
			time.sleep(1)
			self.conn.send(response)
			if viewflag:
				gamescene.update()
			gc.collect()

	def close(self):
		self.conn.close()


if __name__ == "__main__":
	host  = "127.0.0.1"
	port  = 5897
	ai = "ai"
	if len(sys.argv) >= 4: ai = sys.argv[3]
	if len(sys.argv) >= 3: port  = int(sys.argv[2])
	if len(sys.argv) >= 2: host  = sys.argv[1]
	exec ("from %s import AI" % ai)
	client = Client()
	client.connect(host, port)
	client.play(viewflag=False)
	time.sleep(10)	
	client.close()

