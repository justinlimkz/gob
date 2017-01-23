import value 

rank = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9 ,'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

def canDoThis(action, data):
	packet = data.split()
	numBoardCards = int(packet[2])
	numLastActions = int(packet[2+numBoardCards+1])
	numLegalActions = int(packet[2+numBoardCards+1+numLastActions+1])
	
	for i in range(2+numBoardCards+1+numLastActions+1, 2+numBoardCards+1+numLastActions+1+numLegalActions+1):
		if packet[i][0:len(action)] == action:
			return True
	return False

def allIn(data):
	if canDoThis("BET", data):
		return "BET:200\n"
	elif canDoThis("RAISE", data):
		return "RAISE:200\n"
	elif canDoThis("CALL", data):
		return "CALL\n"
	else:
		return "CHECK\n"
	

def getaction(myHand, data):
	num0 = myHand[0][0]
	num1 = myHand[1][0]
	numCards = int(data.split()[2])
	currentCards = data.split()[2:2+numCards]
	pair0 = False
	pair1 = False
	pocket = False
	for card in currentCards:
		if num0 == card[0]:
			pair0 = True
		elif num1 == card[0]:
			pair1 = True
	if num0 == num1:	
		pocket = True
		
	if not (pair0 or pair1 or pocket):
		if canDoThis("DISCARD", data):
			return "DISCARD:"+myHand[1]+"\n"
		else:
			if canDoThis("CALL", data):
				return "CALL\n"
			else:
				return "CHECK\n"
	
	if (pocket or (pair0 and pair1)):
		allIn(data)
	
	if pair0 and canDoThis("DISCARD", data):
		return "DISCARD:"+myHand[1]+"\n"
	if pair1 and canDoThis("DISCARD", data):
		return "DISCARD:"+myHand[0]+"\n"
		
	if canDoThis("CALL", data):
		return "CALL\n"
	return "CHECK\n"