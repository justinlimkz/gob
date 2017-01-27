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
    NO = [-1, -1]
    packet = data.split()
    numBoardCards = int(packet[2])
    boardCards = packet[3:3+numBoardCards]
    numLastActions = int(packet[2+numBoardCards+1])
    numLegalActions = int(packet[2+numBoardCards+1+numLastActions+1])
    
    limit=0
    minBet = 0
    maxBet = 0
    minRaise = 0
    maxRaise = 0    
    
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
                if canDoThis("CHECK", data):   
                    return "CHECK\n"
                return "FOLD\n";
            else:
                bet = minRaise
                
        if packet[i][0:len("CALL")] == "CALL":
            pot = 0
            if packet[2+numBoardCards+1+numLastActions][0:len("POST")] == "POST":
                pot = int(packet[2+numBoardCards+1+numLastActions].split(":")[1])
            elif packet[2+numBoardCards+1+numLastActions][0:len("BET")] == "BET":
                pot = int(packet[2+numBoardCards+1+numLastActions].split(":")[1])
            elif packet[2+numBoardCards+1+numLastActions][0:len("RAISE")] == "RAISE":
                pot = int(packet[2+numBoardCards+1+numLastActions].split(":")[1])
                
            if pot > limit and canDoThis("FOLD", data):
                if canDoThis("CHECK\n", data):
                    return "CHECK\n"
                return "FOLD\n"
            return "CALL\n"
        
        if packet[i][0:len("CHECK")] == "CHECK":
            return "CHECK\n"
            
    return "CHECK\n";