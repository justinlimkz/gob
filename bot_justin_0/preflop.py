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
    
def getAction(myHand, data, times_all_in):
    packet = data.split()
    
    numBoardCards = int(packet[2])
    numLastActions = int(packet[2+numBoardCards+1])
    numLegalActions = int(packet[2+numBoardCards+1+numLastActions+1])
    
    num = [rank[myHand[0][0]], rank[myHand[1][0]]]
    suit = [myHand[0][1], myHand[1][1]]
    currentCards = packet[2:2+numBoardCards]
    
    

    odds =[[85,76,66,65,65,63,62,61,60,60,59,58,57],
           [65,82,63,63,62,60,58,58,57,56,55,54,53],
           [64,61,80,60,59,58,56,54,54,53,52,51,50],
           [64,61,58,77,58,56,54,52,51,50,49,48,47],
           [63,59,57,55,75,54,52,51,49,47,47,46,45],
           [61,58,55,53,52,72,51,49,47,46,44,43,42],
           [60,56,54,51,50,48,69,48,46,45,43,41,40],
           [59,55,52,50,48,46,45,66,45,44,42,40,38],
           [58,54,51,48,46,44,43,42,63,43,41,40,38],
           [58,53,50,47,44,43,41,41,40,60,41,40,38],
           [57,52,49,46,44,41,39,39,38,38,57,39,37],
           [56,51,48,45,43,40,37,37,36,36,35,54,36],
           [55,51,47,44,42,39,37,35,34,34,33,32,50]]

    

    if num[1] > num[0]:
        num[1],num[0] = num[0],num[1]

    score = 0

    if(suit[0] == suit[1]):
        score = odds[14-num[1]][14-num[0]]
    else:
        score = odds[14-num[0]][14-num[1]]

    if data.split()[4] == "POST:1:EzMoney" and score<35:
    #abs(num[0]-num[1]) > 4 and suit[0] != suit[1] and max(num[0], num[1]) < 10:
        return ("FOLD\n" , times_all_in)

    limit = 2

    if(score<=40):
        limit = 2
    elif(score<=50):
        limit = 5
    elif(score<=55):
        limit = 15
    elif(score<=58):
        limit = 25
    elif(score<=60):
        limit = 50
    elif(score<=63):
        limit = 100
    elif(score<=65):
        limit = 150
    elif(score<=100):
        limit = 200
        
        
    
    '''limit = 6*max(num[0], num[1])
    
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
        limit *= 2.0'''
    
    minBet = 99999
    maxBet = -99999
    minRaise = 99999
    maxRaise = -99999
    pot = 0
    
    for i in range(2+numBoardCards+1+numLastActions+1+1, 2+numBoardCards+1+numLastActions+1+numLegalActions+1):
        if packet[i][0:len("BET")] == "BET":
            minBet = int(packet[i].split(":")[1])
            maxBet = int(packet[i].split(":")[2])
        if packet[i][0:len("RAISE")] == "RAISE":    
            minRaise = int(packet[i].split(":")[1])
            maxRaise = int(packet[i].split(":")[2])
        if packet[i][0:len("CALL")] == "CALL":
            
            if packet[2+numBoardCards+1+numLastActions][0:len("POST")] == "POST":
                pot = int(packet[2+numBoardCards+1+numLastActions].split(":")[1])
            elif packet[2+numBoardCards+1+numLastActions][0:len("BET")] == "BET":
                pot = int(packet[2+numBoardCards+1+numLastActions].split(":")[1])
            elif packet[2+numBoardCards+1+numLastActions][0:len("RAISE")] == "RAISE":
                pot = int(packet[2+numBoardCards+1+numLastActions].split(":")[1])
        
    #print (limit)
    rng = random.uniform(0, 100)
 #   limit += 100
    #Priority in order: BET, RAISE, CALL, CHECK

    if(pot < 50 and maxRaise - minRaise <= 10 ):
        times_all_in += 1.0
    else:
        times_all_in -= 0.5

    if(times_all_in >= 50.0):
        if limit > 149:
            return ("CALL\n" , times_all_in)
        else:
            return ("CHECK\n" , times_all_in)

    if canDoThis("BET", data):
        multiplier = 0.75 #default?
        if 0<rng<=5:
            multiplier = 1
        if 5<rng<=10:
            multiplier = 0.75
        if 10<rng<=20:
            multiplier = 0.50
        if 20<rng<=30:
            multiplier = 0.33
        if 30<rng<=45:
            multiplier = 0.25
        if 45<rng<=55:
            multiplier = 0 #minBet
        if 55<rng<=100:
            if canDoThis("CHECK\n", data):
                return ("CHECK\n" , times_all_in)
        
        bet = max(limit*(multiplier), minBet)
        bet = min(bet, maxBet)
        bet = int(bet)
        if minBet <= limit:
            return ("BET:" + str(bet) + "\n" , times_all_in)

    if canDoThis("RAISE", data):
        multiplier = 1
        if 0<rng<=5:
            multiplier = 1
        if 5<rng<=10:
            multiplier = 0.75
        if 10<rng<=20:
            multiplier = 0.50
        if 20<rng<=30:
            multiplier = 0.33
        if 30<rng<=45:
            multiplier = 0.25
        if 45<rng<=55:
            multiplier = 0 #minRaise
        if 55<rng<=100:
            if canDoThis("CHECK", data):
                return ("CHECK\n" , times_all_in)
            if(maxRaise - minRaise <= 25):
                return ("CALL\n" , times_all_in)
        
        if minRaise <= limit:
            bet = max(limit*multiplier, minRaise)
            return ("RAISE:" + str(int(bet)) + "\n"  , times_all_in)   

    if canDoThis("CALL", data):
        if pot <= limit or (maxRaise - minRaise <= 25 and pot>300-limit):
            return ("CALL\n" , times_all_in)
        
    return ("CHECK\n" , times_all_in)
        
