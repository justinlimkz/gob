def canDoThis(action, data):
    packet = data.split()
    numBoardCards = int(packet[2])
    numLastActions = int(packet[2+numBoardCards+1])
    numLegalActions = int(packet[2+numBoardCards+1+numLastActions+1])
    
    for i in range(2+numBoardCards+1+numLastActions+1+1, 2+numBoardCards+1+numLastActions+1+numLegalActions+1):
        if packet[i][0:len(action)] == action:
            return True
    return False
    
def getAction(myHand, data, modify):
    if canDoThis("BET", data):
        return "BET:200\n"
    if canDoThis("RAISE", data):
        return "RAISE:200\n"
    return "CALL\n"
