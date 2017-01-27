import value 

rank = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9 ,'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

def canDoThis(action, data):
	packet = data.split()
	numBoardCards = int(packet[2])
	numLastActions = int(packet[2+numBoardCards+1])
	numLegalActions = int(packet[2+numBoardCards+1+numLastActions+1])
	
	for i in range(2+numBoardCards+1+numLastActions+1+1, 2+numBoardCards+1+numLastActions+1+numLegalActions+1):
		if packet[i][0:len(action)] == action:
			return True
	return False
	
def getAction(myHand, data):
	packet = data.split()
	
	numBoardCards = int(packet[2])
	numLastActions = int(packet[2+numBoardCards+1])
	numLegalActions = int(packet[2+numBoardCards+1+numLastActions+1])
	
	num = [rank[myHand[0][0]], rank[myHand[1][0]]]
	suit = [myHand[0][1], myHand[1][1]]
	currentCards = packet[2:2+numBoardCards]
	
	if data.split()[4] == "POST:1:EzMoney" and abs(num[0]-num[1]) > 4 and suit[0] != suit[1] and max(num[0], num[1]) < 10:
		return "FOLD\n"
	
	limit = 6*max(num[0], num[1])
	
	if suit[0] == suit[1]:
		limit *= 1.5
	if abs(num[0]-num[1]) == 4:
		limit *= 1.1
	if abs(num[0]-num[1]) == 3:
		limit *= 1.2
	if abs(num[0]-num[1]) == 2:
		limit *= 1.3
	if abs(num[0]-num[1]) == 1:
		limit *= 1.4
	if num[0] == num[1]:
		limit *= 2.0
	
	for i in range(2+numBoardCards+1+numLastActions+1+1, 2+numBoardCards+1+numLastActions+1+numLegalActions+1):
		if packet[i][0:len("BET")] == "BET":
			minBet = int(packet[i].split(":")[1])
			maxBet = int(packet[i].split(":")[2])
			bet = max(limit*(0.75), minBet)
			bet = min(bet, maxBet)
			bet = int(bet)
			return "BET:" + str(bet) + "\n"
			
		if packet[i][0:len("RAISE")] == "RAISE":	
			minRaise = int(packet[i].split(":")[1])
			maxRaise = int(packet[i].split(":")[2])
			if minRaise > limit and canDoThis("FOLD", data):
			    if canDoThis("CHECK\n", data):
			        return "CHECK\n"
				return "FOLD\n";
			else:
				bet = minRaise
				if num[0] == num[1]:
					bet = 30+5*num[0]
				return "RAISE:" + str(bet) + "\n"	
		
		if packet[i][0:len("CALL")] == "CALL":
			pot = 0
			if packet[2+numBoardCards+1+numLastActions][0:len("POST")] == "POST":
				pot = int(packet[2+numBoardCards+1+numLastActions].split(":")[1])
			elif packet[2+numBoardCards+1+numLastActions][0:len("BET")] == "BET":
				pot = int(packet[2+numBoardCards+1+numLastActions].split(":")[1])
			elif packet[2+numBoardCards+1+numLastActions][0:len("RAISE")] == "RAISE":
				pot = int(packet[2+numBoardCards+1+numLastActions].split(":")[1])
				
			if pot > limit and canDoThis("FOLD", data):
				return "FOLD\n"
			return "CALL\n"
		
		if packet[i][0:len("CHECK")] == "CHECK":
			return "CHECK\n"
			
	return "CHECK\n";
		