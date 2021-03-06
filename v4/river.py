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

def getAction(myHand, data, modify):
    NO = [-1, -1]
    packet = data.split()
    numBoardCards = int(packet[2])
    boardCards = packet[3:3+numBoardCards]
    numLastActions = int(packet[2+numBoardCards+1])
    numLegalActions = int(packet[2+numBoardCards+1+numLastActions+1])
    
    limit=0
    minBet = 99999
    maxBet = -99999
    minRaise = 99999
    maxRaise = -99999
    
    for i in range(2+numBoardCards+1+numLastActions+1+1, 2+numBoardCards+1+numLastActions+1+numLegalActions+1):
        if packet[i][0:len("BET")] == "BET":
            minBet = int(packet[i].split(":")[1])
            maxBet = int(packet[i].split(":")[2])
            bet = max(limit*(0.75), minBet)
            bet = min(bet, maxBet)
            bet = int(bet)
        if packet[i][0:len("RAISE")] == "RAISE":    
            minRaise = int(packet[i].split(":")[1])
            maxRaise = int(packet[i].split(":")[2])
            
    
    MaxBet=str(maxBet)
    MaxRaise=str(maxRaise)
    hand=value.get_full_hand(data,myHand)
    if value.is_royal(hand) != NO or value.is_flush(hand) != NO or value.is_of_a_kind(hand)[0] == 7 or value.is_full_house(hand)[0] == 6 or value.is_straight(hand) != NO:
        if canDoThis("RAISE",data): 
            return "RAISE:"+MaxRaise+"\n"
        elif canDoThis("BET", data):
            return "BET:"+MaxBet+"\n"
    elif value.is_full_house(hand)[0]==2:
        if value.count_same_suit(boardCards)[0]==4 or value.double_sided_straight(boardCards)!=False:
            limit=25
        elif value.is_full_house(hand)[1] in myHand:
            if canDoThis("RAISE",data):
                return "RAISE"+MaxRaise+"\n"
            elif canDoThis("BET",data):
                return "BET"+MaxBet+"\n"
        else:
            limit=25
    elif value.is_of_a_kind(hand)[0]==1:
        if value.is_of_a_kind(hand)[1] in myHand:
            if value.count_same_suit(boardCards)[0]==4 or value.double_sided_straight(boardCards)[0]!=False:
                limit=30
            else:
                pair_card=value.is_of_a_kind(hand)[1]
                rank=1
                for i in boardCards:
                    if pair_card<i:
                        rank+=1
                limit=6*pair_card+(5-rank)*40
                if limit>200:
                    limit=200
        else:
            limit=15
    elif value.count_same_suit(boardCards)[0]==4 or value.double_sided_straight(boardCards)!=False:
        limit=0
    else:
        limit=value.high(hand)[1]*3
        
    if int (limit * modify)>limit:
        limit = int (limit * modify)

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
        

    rng = random.uniform(0, 100)
    #Priority in order: BET, RAISE, CALL, CHECK

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
                return "CHECK\n"
        
        bet = max(limit*(multiplier), minBet)
        bet = min(bet, maxBet)
        bet = int(bet)
        if minBet <= limit:
            return "BET:" + str(bet) + "\n"

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
                return "CHECK\n"
            if(pot>300-limit):
                return "CALL\n"
        
        bet = max(limit*multiplier, minRaise)
        bet = min(bet, maxRaise)
        bet = int(bet)
        if minRaise <= limit:
            return "RAISE:" + str(bet) + "\n"       

    if canDoThis("CALL", data):
        if pot <= limit or pot>300-limit:
            return "CALL\n"
        
    return "CHECK\n";
