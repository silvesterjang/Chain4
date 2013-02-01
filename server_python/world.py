import random

class World(object):
	def __init__(self, row = 16, col = 16):
		self.map = [[0 for i in xrange(col)] for j in xrange(row)]
		self.row = row
		self.col = col
	
	def initial(self, times):
		for i in range(times):
			select = random.randrange(0,16)
			self.put(select, 3)

	def put(self, row, player):
		result = False #If this value returns, winner function calculate (player, false) returns
		col = 987654321 # INF
		
		for i in xrange(len(self.map[row])): # For each selected row, it search appropriate place to put block
			if self.map[row][i] == 0 : # empty place
				result = True # we can put block in empty place
				col = i
				break # finish

		if not result : 
			return (player, result)

		self.map[row][col] = player
		return (player, result)

	def eval(self):
		map_rows = self.row
		map_cols = self.col
		count = 3
		def subproblem(player,row,col,count,direction):
			if count == 0:
				return (player,True)
			if direction == 0 : # East
				if col >= map_cols - count :
					return (player, False)
				if self.map[row][col+1] != player :
					return (player, False)
				return subproblem(player,row,col+1,count-1,direction)
			elif direction == 1 : # East & South
				if col >= map_cols - count or row >= map_rows - count :
					return (player, False)
				if self.map[row+1][col+1] != player :
					return (player, False)
				return subproblem(player,row+1,col+1,count-1,direction)
			elif direction == 2 : # South
				if row >= map_rows - count : 
					return (player, False)
				if self.map[row+1][col] != player :
					return (player, False)
				return subproblem(player,row+1,col, count-1,direction)
			elif direction == 3 : # West & South
				if row >= map_rows - count or col < count :
					return (player, False)
				if self.map[row+1][col-1] != player :
					return (player, False)
				return subproblem(player,row+1,col-1,count-1,direction)
		
		result = []
		for i in range(map_rows):
			for j in range(map_cols):
				player = self.map[i][j]
				if player != 0 and player != 3:
					for direction in range(4):
						result.append(subproblem(player,i,j,3,direction))

		return result
						
	def winner(self):
		result = self.eval()
		val = 987654321 # INF
		for i in range(len(result)):
			if result[i][1] == True:
				return result[i][0]
		return val

	def is_empty(self):
		val = -1 # 16*16
		for i in range(len(self.map)):
			for j in range(len(self.map[i])) : #for each row
				if self.map[i][j] == 0 :
					val = 1
					return val
		return val
