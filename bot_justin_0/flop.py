import value 
import random

rank = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9 ,'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

NO = [-1, -1]

limit = 0

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
    
    board = packet[3:3+numBoardCards]
    combined = myHand+board
    
    if canDoThis("DISCARD", data):
        if value.is_flush(combined) != NO or value.is_straight(combined) != NO or value.is_full_house(combined)[0] == 6 or value.is_of_a_kind(combined)[0] == 7:
            
            if value.is_of_a_kind(combined)[0] == 7 and myHand[0][0] != myHand[1][0]: 
                #four of a kind but only uses one card in hand
                if myHand[0][0] == board[0][0]:
                    return "DISCARD:" + myHand[1] + '\n'
                else:
                    return "DISCARD:" + myHand[0] + '\n'
            else:
                return "CHECK\n"
              
        if value.count_same_suit(combined)[0] == 4:
            suit = value.count_same_suit(combined)[1]
            if myHand[0][1] == suit and myHand[1][1] == suit:
                return "CHECK\n"
            elif myHand[0][1] == suit:
                return "DISCARD:" + myHand[1] + '\n'
            else:
                return "DISCARD:" + myHand[0] + '\n'
                
        if value.double_sided_straight(combined) != False:
            low_card = value.double_sided_straight(combined)
            if(low_card <= myHand[0] <= low_card + 3 and low_card <= myHand[1] <= low_card + 3): #both cards
                return "CHECK\n"
            elif(low_card <= myHand[0] <= low_card + 3): #one card
                return "DISCARD:" + myHand[1] + '\n'
            elif(low_card <= myHand[1] <= low_card + 3): #one card
                return "DISCARD:" + myHand[0] + '\n'

        if value.hole_straight(combined) != False:
            low_card = value.hole_straight(combined)
            if(low_card <= myHand[0][0] <= low_card + 4 and low_card <= myHand[1][0] <= low_card + 4):#both cards
                if(9 > myHand[0][0] < myHand[1][0]):
                    return "DISCARD:" + myHand[0] + '\n'
                elif(9 > myHand[1][0] < myHand[0][0]):
                    return "DISCARD:" + myHand[0] + '\n'
                else:
                    return "CHECK\n"
            elif(low_card <= myHand[0][0] <= low_card + 4): #one card
                if(value.is_of_a_kind(board+myHand[0])[0] >= 1): #at least a pair made from board & first card
                    return "DISCARD:" + myHand[1] + '\n'
                else:
                    return "CHECK\n"
            elif(low_card <= myHand[1][0] <= low_card + 4): #one card
                if(value.is_of_a_kind(board+myHand[1])[0] >= 1): #at least a pair made from board & first card
                    return "DISCARD:" + myHand[0] + '\n'
                else:
                    return "CHECK\n"
        
        if value.is_of_a_kind(combined)[0] == 3:
            if myHand[0][0] != myHand[1][0]:
                if myHand[0][0] == value.is_of_a_kind(combined)[1]:
                    return "DISCARD:" + myHand[1] + '\n'
                else:
                    return "DISCARD:" + myHand[0] + '\n'
            else:
                return "CHECK\n";
        
        if value.is_full_house(combined)[0] == 2: #two pair
            if myHand[0][0] == myHand[1][0]:
                if rank[myHand[0][0]] < min(rank[board[0][0]], rank[board[1][0]], rank[board[2][0]]):
                    return "DISCARD:" + myHand[0] + '\n'
                else:
                    return "CHECK\n"
            elif myHand[0][0] in [board[0][0], board[1][0], board[2][0]] and myHand[1][0] in [board[0][0], board[1][0], board[2][0]]:
                return "CHECK\n"
            else:
                if myHand[0][0] in [board[0][0], board[1][0], board[2][0]]:
                    return "DISCARD:" + myHand[1] + '\n' 
                else:
                    return "DISCARD:" + myHand[0] + '\n'
    
        if value.is_of_a_kind(combined)[0] == 1:
            cards_sorted = sorted(combined, key=lambda x: x[0])
            if myHand[0][0] == myHand[1][0]:
                if(myHand[0][0] == cards_sorted[0][0]):
                    return "DISCARD:" + myHand[0] + '\n'
                else:
                    return "CHECK\n"
            else:
                if value.is_of_a_kind(combined)[1] == rank[myHand[0][0]]:
                    return "DISCARD:" + myHand[1] + '\n'
                if value.is_of_a_kind(combined)[1] == rank[myHand[1][0]]:
                    return "DISCARD:" + myHand[0] + '\n'
        
        if rank[myHand[0][0]] < rank[myHand[1][0]]:
            return "DISCARD:" + myHand[0] + '\n'
        
        if rank[myHand[0][0]] > rank[myHand[1][0]]:
            return "DISCARD:" + myHand[1] + '\n'
        
        return "CHECK\n"
        
    else:
        
        limit = 10
        
        if value.is_flush(combined) != NO or value.is_straight(combined) != NO or value.is_full_house(combined)[0] == 6 or value.is_of_a_kind(combined)[0] == 7: #full house and higher
            limit = 200
        
        elif value.is_of_a_kind(combined)[0] == 3: #triple
            if myHand[0][0] == value.is_of_a_kind(combined)[1] or myHand[1][0] == value.is_of_a_kind(combined)[1]:
                limit = 200
            else:
                limit = 70
                    
                    
        elif value.is_full_house(combined)[0] == 2: #two pair
            if myHand[0][0] == myHand[1][0]:
                if rank[myHand[0][0]] > max(rank[board[0][0]], rank[board[1][0]], rank[board[2][0]]):
                    limit = 200
                else:
                    limit = 80
            result = value.is_full_house(combined)
            if (result[1][0] == myHand[0][0] and result[1][1] == myHand[1][0]) or (result[1][1] == myHand[0][0] and result[1][0] == myHand[1][0]):
                limit = 200
            elif (result[1][0] == myHand[0][0] or result[1][0] == myHand[1][0]):
                limit = 200
            elif (result[1][0] == myHand[0][0] or result[1][0] == myHand[1][0]):
                limit = 100
            else:
                limit = 40

        elif value.is_of_a_kind(combined)[0] == 1: #one pair
            if(myHand[0][0] == myHand[1][0] == value.is_of_a_kind(combined)[1]):
                if rank[myHand[0][0]] >= 10:
                    limit = 15*rank[myHand[0][0]]
                elif rank[myHand[0][0]] >= 6:
                    limit = 5*rank[myHand[0][0]]
                else:
                    limit = 10                
            elif myHand[0][0] in [board[0][0], board[1][0], board[2][0]]:
                limit = min(6*rank[myHand[0][0]]+(4-rank[myHand[0][0]]),100)
            elif myHand[1][0] in [board[0][0], board[1][0], board[2][0]]:
                limit = min(6*rank[myHand[1][0]]+(4-rank[myHand[1][0]]),100)
            else:
                limit = 5 + max(rank[myHand[0][0]], rank[myHand[1][0]])

        else:
            limit = 5 + max(rank[myHand[0][0]], rank[myHand[1][0]])

        if value.count_same_suit(combined)[0] == 4:
            the_suit = value.count_same_suit(combined)[1]
            if myHand[0][1] == myHand[1][1] == the_suit:
                limit = 90
            elif myHand[0][1] == the_suit:
                if myHand[0][0] >= 13: #A or K
                    limit = 60
                elif myHand[0][0] >= 9:
                    limit = 40
                else:
                    limit = 15
            elif myHand[1][1] == the_suit:
                if myHand[1][0] >= 13: #A or K
                    limit = 60
                elif myHand[1][0] >= 9:
                    limit = 40
                else:
                    limit = 15

        if value.double_sided_straight(combined) != False:
            low_card = value.double_sided_straight(combined)
            if(low_card <= myHand[0] <= low_card + 3 and low_card <= myHand[1] <= low_card + 3): #both cards
                limit = 50
            elif(low_card <= myHand[0] <= low_card + 3 or low_card <= myHand[1] <= low_card + 3): #one card
                limit = 25
                
        elif value.hole_straight(combined) != False:
            low_card = value.double_sided_straight(combined)
            if(low_card <= myHand[0][0] <= low_card + 4 and low_card <= myHand[1][0] <= low_card + 4):#both cards
                limit = 30
            elif(low_card <= myHand[0][0] <= low_card + 4 or low_card <= myHand[1][0] <= low_card + 4): #one card
                limit = 15

        #print(limit) ##########
        #print (str(limit) + '\n\n')

        minBet = 0
        maxBet = 1
        minRaise = 0
        maxRaise = 1
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
        limit += 100
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
                if((maxRaise - minRaise <= 25 and pot>300-limit)):
                    return "CALL\n"
        
            
            bet = max(limit*multiplier, minRaise)
            bet = min(bet, maxRaise)
            bet = int(bet)
            if minRaise <= limit:
                return "RAISE:" + str(bet) + "\n"    

        if canDoThis("CALL", data):
            if pot <= limit or (maxRaise - minRaise <= 25 and pot>300-limit):
                return "CALL\n"

        return "CHECK\n";
