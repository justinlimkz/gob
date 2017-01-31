import value 
import random

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
    
    for lastAction in packet[2+numBoardCards+2:2+numBoardCards+2+numLastActions]:
        if "RAISE" in lastAction:
            return "FOLD\n"
    
    return "RAISE:4\n"
        
