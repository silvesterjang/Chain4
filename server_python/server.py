import socket, sys, gc, re, time, random
from world import World
from gamescene import Gamescene

class Server(object):
	def __init__ (self, port):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind(("",port))
		self.server.listen(2) # Accept two client
	
	def listen(self):
		self.conn = [None] * 3
		self.conn[1], addr1 = self.server.accept()
		self.conn[1].send("%d %d 1\n" % (self.world.row, self.world.col))
		self.name1 = self.conn[1].recv(1024).strip()
		self.conn[2], addr2 = self.server.accept()
		self.conn[2].send("%d %d 2\n" % (self.world.row, self.world.col))
		self.name2 = self.conn[2].recv(1024).strip()
		self.conn[1].send("%s\n" % self.name2)
		self.conn[2].send("%s\n" % self.name1)
		print "RED  : %s from %s" % (self.name1, addr1[0])
		print "BLUE : %s from %s" % (self.name2, addr2[0])

		
	def update(self, rows, player):
		row = rows.split()
		for i in xrange(0, len(row)):
			self.world.put(int(row[i]), player)
	
	def close(self):
		self.conn[1].close()
		self.conn[2].close()

	def play(self, maxturn = 1000, gamescene=None):
		chance = [None,2,2]
		UsedChance = [None,False,False]

		wait_time = 0.3
		player = 0

		for turn in xrange(maxturn):
			if self.world.is_empty() == -1: #is not empty
				self.conn1.send("DRAW\n")
				self.conn2.send("DRAW\n")
				break

			mapinfo = re.sub("[[]|[]]|,| ","",str(self.world.map))
			if turn % 2 == 0 : # even turn -> Player 1 : RED
				player = 1
			else : # odd turn -> Player 2 : Blue
				player = 2

			self.conn[player].send(str(turn)+" "+mapinfo+"\n")
			
			#start to time bound check < 3 second
			start = time.time()
			recvdata = self.conn[player].recv(1024).strip().split(' ')
			end = time.time()
			if end-start >= 3:
				self.conn[player].send("LOSE")
				self.conn[3-player].send("WIN")
				break

			if recvdata[0] == "PASS":
				UsedChance[player] = False
			elif recvdata[0] == "PUT":
				UsedChance[player] = False
				select_row = int(recvdata[1])
				if self.world.map[select_row][self.world.col - 1] != 0:
					self.conn[player].send("LOSE")
					self.conn[3-player].send("WIN")
					break
				#else
				self.world.put(select_row,player)
			elif recvdata[0] == "CHANCE":
				select_row1 = int(recvdata[1])
				select_row2 = int(recvdata[2])
				#Does he/she use his chance before his/her turn?
				if UsedChance[player] == True or chance[player] < 1 or self.world.map[select_row1][self.world.col - 1] != 0 or self.world.map[select_row2][self.world.col - 1] != 0:
					self.conn[player].send("LOSE")
					self.conn[3-player].send("WIN")
					break
				#else...
				UsedChance[player] = True
				chance[player] -= 1
				self.world.put(select_row1,player)
				self.world.put(select_row2,player)

			time.sleep(wait_time)
			
			if gamescene != None:
				gamescene.set_caption("Chain 4 (%s vs. %s) - Turn: %d" % (self.name1, self.name2, turn+1))
				gamescene.update()

			result = self.world.winner()

			gc.collect()

			if result == 1:
				self.conn[1].send("WIN")
				self.conn[2].send("LOSE")
				print "RED WIN"
				break
			elif result == 2:
				self.conn[1].send("LOSE")				
				self.conn[2].send("WIN")
				print "BLUE WIN"
				break
			else:
				print "KEEP GOING"


if __name__ == "__main__":
	if len(sys.argv) >= 2:
		port = int(sys.argv[1])
	else:
		port = 5897
	server = Server(port)
	while True:
		print "Server is opened"
		server.world = World()
		randomnum = random.randint(10,13)
		server.world.initial(randomnum)
		server.listen()
		server.play(gamescene=Gamescene(server.world), maxturn=1000)
		server.close()
		time.sleep(10)			
