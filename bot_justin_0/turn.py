import value

def canDoThis(action, data):
	packet = data.split()
	numBoardCards = int(packet[2])
	numLastActions = int(packet[2+numBoardCards+1])
	numLegalActions = int(packet[2+numBoardCards+1+numLastActions+1])
	
	for i in range(2+numBoardCards+1+numLastActions+1+1, 2+numBoardCards+1+numLastActions+1+numLegalActions+1):
		if packet[i][0:len(action)] == action:
			return True
return False


rank = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9 ,'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

def getAction(myHand, data):
    royal_check = value.is_royal(hand)
    full_value = value.is_full_house(hand)
    pair_value = value.is_of_a_kind(hand)
    flush_value = value.is_flush(hand)
    straight_value = value.is_straight(hand)
    high_value = value.high(hand)
    if royal_check[0] == 9 or royal_check[0] == 8 or pair_value[0] == 7 or full_value[0] == 6 or flush_value[0] == 5 or straight_value[0] == 4:
        return "RAISE:" #Define what is meant by "lead in"
    if pair_value[0] == 3 or full_value[0] == 2: #Triple or Two Pair
        return "RAISE:200\n"
    if pair_value[0] == 1: #Pair
    if high_value[0] == 0: #High Card
    
    