import socket, sys, gc, re, time
from world import World
from gamescene import Gamescene

class Server(object):
	def __init__ (self, port):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind(("",port))
		self.server.listen(2) # Accept two client

	def world(self, world):
		self.world = world
	
	def listen(self):
		self.conn1, addr1 = self.server.accept()
		self.conn1.send("%d %d 1\n" % (self.world.row, self.world.col)) #an information of world map
		self.name1 = self.conn1.recv(1024).strip()

		self.conn2, addr2 = self.server.accept()
		self.conn2.send("%d %d 2\n" % (self.world.row, self.world.col))
		self.name2 = self.conn2.recv(1024).strip()

		self.conn1.send("%s\n" % self.name2)
		self.conn2.send("%s\n" % self.name1)

		print "RED :", self.name1, "from", addr1[0]
		print "BLUE :", self.name2, "from", addr2[0]
		
	def update(self, rows, player):
		row = rows.split()
		for i in xrange(0, len(row)):
			self.world.put(int(row[i]), player)
	
	def close(self):
		self.conn1.close()
		self.conn2.close()

	def cleanup(self):
		self.server.close()

	def player1win(self):
		self.conn1.send("WIN\n")
		self.conn2.send("LOSE\n")

	def player2win(self):
		self.conn1.send("LOSE\n")
		self.conn2.send("WIN\n")

	def play(self, maxturn = 1000, gamescene=None):
		player1chance = 2
		player2chance = 2
		player1UsedHisHerChance = False
		player2UsedHisHerChance = False

		player = 0
		for turn in xrange(maxturn):
			print "---------Status----------"
			print "%d turn : Player %d do something" %(turn + 1, ((turn % 2) + 1))
			print "Player 1 final attack remains : %d, Use final attack before turn : %s " %(player1chance, str(player1UsedHisHerChance))
			print "Player 2 final attack remains : %d, Use final attack before turn : %s " %(player2chance, str(player2UsedHisHerChance))
			print "-------------------------"

			if self.world.is_empty() == -1: #is not empty
				self.conn1.send("DRAW\n")
				self.conn2.send("DRAW\n")
				sys.exit()

			mapinfo = re.sub("[[]|[]]|,| ","",str(self.world.map))
			"""
			It throws one line map information to user 
			ex)
			0123
			4567
			8901 -> 012345678901
			"""
			if turn % 2 == 0 : # even turn -> Player 1
				player = 1
				self.conn1.send(str(turn)+" "+mapinfo+"\n")
				recvdata = self.conn1.recv(1024).strip().split(" ")

				# User request
				if recvdata[0] == "PASS":
					if player1UsedHisHerChance == True :
						player1UsedHisHerChance = False
					pass

				elif recvdata[0] == "PUT":
					if player1UsedHisHerChance == True :
						player1UsedHisHerChance = False

					select_row = int(recvdata[1])
					if self.world.map[select_row][self.world.col - 1] != 0 : # If there is no space to put block, player 1 must lose.
						self.player2win()
					
					# Test is all clear
					self.world.put(select_row, player)

				elif recvdata[0] == "CHANCE":
					"""
					Player 1 and Player 2 have two final attack, for each final attack player can put 2 block. However player cannot use sequentially. if user use it once, after one his/her turn can use it.  
					"""
					# Check
					if player1chance <= 0 or player1UsedHisHerChance == True:
						self.player2win()
					
					# Check
					select_row1 = int(recvdata[1])
					select_row2 = int(recvdata[2])
					if self.world.map[select_row1][self.world.col - 1] != 0 or self.world.map[select_row2][self.world.map.col - 1] != 0: # each row is already full.
						self.player2win()
					self.world.put(select_row1, player)
					self.world.put(select_row2, player)
					player1chance = player1chance - 1
					player1UsedHisHerChance = True

			else : # odd turn -> Player 2
				player = 2
				self.conn2.send(str(turn)+" "+mapinfo+"\n")
				recvdata = self.conn2.recv(1024).strip().split(" ")

				# User request
				if recvdata[0] == "PASS":
					if player2UsedHisHerChance == True :
						player2UsedHisHerChance = False
					pass

				elif recvdata[0] == "PUT":
					if player2UsedHisHerChance == True :
						player2UsedHisHerChance = False

					select_row = int(recvdata[1])
					if self.world.map[select_row][self.world.col - 1] != 0 : # If there is no space to put block, player 1 must lose.
						self.player1win()
					
					# Test is all clear
					self.world.put(select_row, player)

				elif recvdata[0] == "CHANCE":
					"""
					Player 1 and Player 2 have two final attack, for each final attack player can put 2 block. However player cannot use sequentially. if user use it once, after one his/her turn can use it.  
					"""
					# Check
					if player2chance <= 0 or player2UsedHisHerChance == True:
						self.player1win()
					
					# Check
					select_row1 = int(recvdata[1])
					select_row2 = int(recvdata[2])
					if self.world.map[select_row1][self.world.col - 1] != 0 or self.world.map[select_row2][self.world.map.col - 1] != 0: # each row is already full.
						self.player2win()
					self.world.put(select_row1, player)
					self.world.put(select_row2, player)
					player2chance = player2chance - 1
					player2UsedHisHerChance = True
			
			if gamescene != None:
				gamescene.set_caption("Chain Chain 4 (%s vs. %s) - Turn: %d" % (self.name1, self.name2, turn+1))
				gamescene.update()

			result = self.world.winner()

			gc.collect()

			if result == 1:
				self.player1win()
				print "RED WIN"
			elif result == 2:
				self.player2win()
				print "BLUE WIN"
			else:
				print "KEEP GOING"


if __name__ == "__main__":
	if len(sys.argv) >= 2:
		port = int(sys.argv[1])
	else:
		port = 5897
	server = Server(port)
	while True:
		try:
			world = World()
			server.world(world)
			server.listen()
			server.play(gamescene=Gamescene(world), maxturn=1000)
			time.sleep(10)			
			server.close()
		except:
			print "Game Over."
			server.cleanup()
			sys.exit(0)
