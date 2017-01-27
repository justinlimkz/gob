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

NO = [-1, -1]

def getAction(myHand, data):
    rank = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9 ,'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

    packet = data.split()
    
    numBoardCards = int(packet[2])
    numLastActions = int(packet[2+numBoardCards+1])
    numLegalActions = int(packet[2+numBoardCards+1+numLastActions+1])
    
    board = packet[3:3+numBoardCards]
    combined = myHand+board
    
    if canDoThis("DISCARD", data):
        if value.is_flush(combined) != NO or value.is_straight(combined) != NO or value.is_full_house(combined)[0] == 6 or value.is_of_a_kind(combined)[0] == 7:
            if value.is_of_a_kind(combined)[0] == 7: #four of a kind
                if rank[myHand[0][0]] == value.is_of_a_kind(combined)[1] and rank[myHand[1][0]] == value.is_of_a_kind(combined)[1]:
                    return "CHECK\n"
                elif rank[myHand[0][0]] == value.is_of_a_kind(combined)[1]: #one card
                    return "DISCARD:" + myHand[1] + '\n'
                elif rank[myHand[1][0]] == value.is_of_a_kind(combined)[1]: #one card
                    return "DISCARD:" + myHand[0] + '\n'
                elif rank[myHand[0][0]] < rank[myHand[1][0]]: #discard lower card
                    return "DISCARD:" + myHand[0] + '\n'
                else:
                    return "DISCARD:" + myHand[1] + '\n'
                
            if value.is_flush(combined) != NO:
                if value.is_flush(board+[myHand[0]]) != NO: #discard card that is not part of flush
                    return "DISCARD:" + myHand[1] + '\n'
                elif value.is_flush(board+[myHand[1]]) != NO:
                    return "DISCARD:" + myHand[0] + '\n'
                else:
                    return "CHECK\n"
                    
            if value.is_straight(combined) != NO:
                if value.is_straight(board+[myHand[0]]) != NO: #discard card that is not part of straight
                    return "DISCARD:" + myHand[1] + '\n'
                elif value.is_straight(board+[myHand[1]]) != NO:
                    return "DISCARD:" + myHand[0] + '\n'
                else:
                    return "CHECK\n"
            
            if value.is_full_house(combined) == 6:
                if value.is_full_house(board+[myHand[0]]) != NO: #discard card that is not part of full house
                    return "DISCARD:" + myHand[1] + '\n'
                elif value.is_full_house(board+[myHand[1]]) != NO:
                    return "DISCARD:" + myHand[0] + '\n'
                else:
                    return "CHECK\n"
                
        if value.count_same_suit(combined)[0] == 4:
            suit = value.count_same_suit(combined)[1]
            if myHand[0][1] == suit and myHand[1][1] == suit: #if both cards part of flush, don't discard
                return "CHECK\n"
            elif myHand[0][1] == suit: #discard other card
                return "DISCARD:" + myHand[1] + '\n'
            elif myHand[1][1] == suit:
                return "DISCARD:" + myHand[0] + '\n'
            else: 
                if myHand[0][0] == myHand[1][0]: #if pair, don't discard
                    return "CHECK\n"
                elif myHand[0][0] in [board[0][0], board[1][0], board[2][0], board[3][0]]: #if pair, discard other card
                    return "DISCARD:" + myHand[1] + '\n'
                elif myHand[1][0] in [board[0][0], board[1][0], board[2][0], board[3][0]]:
                    return "DISCARD:" + myHand[0] + '\n' 
                elif rank[myHand[0][0]] > rank[myHand[1][0]]: #discard lower card
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
            else:
                if myHand[0][0] == myHand[1][0]:
                    return "CHECK\n"
                elif myHand[0][0] in [board[0][0], board[1][0], board[2][0], board[3][0]]:
                    return "DISCARD:" + myHand[1] + '\n'
                elif myHand[1][0] in [board[0][0], board[1][0], board[2][0], board[3][0]]:
                    return "DISCARD:" + myHand[0] + '\n' 
                elif rank[myHand[0][0]] > rank[myHand[1][0]]:
                    return "DISCARD:" + myHand[1] + '\n'
                else:
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
            elif rank[myHand[0][0]] > rank[myHand[1][0]]: #discard lower card
                return "DISCARD:" + myHand[1] + '\n'
            else:
                return "DISCARD:" + myHand[0] + '\n'

        if value.is_of_a_kind(combined)[0] == 3:
            if myHand[0][0] != myHand[1][0]: 
                if rank[myHand[0][0]] == value.is_of_a_kind(combined)[1]: #if one card isn't part of triple, discard other card
                    return "DISCARD:" + myHand[1] + '\n'
                elif rank[myHand[1][0]] == value.is_of_a_kind(combined)[1]:
                    return "DISCARD:" + myHand[0] + '\n'
                elif rank[myHand[0][0]] > rank[myHand[1][0]]: #discard lower card
                    return "DISCARD:" + myHand[1] + '\n'
                else:
                    return "DISCARD:" + myHand[0] + '\n'
            else: #stay if pockets
                return "CHECK\n";
        
        if value.is_full_house(combined)[0] == 2: #two pair
            if myHand[0][0] == myHand[1][0]: #pockets
                if rank[myHand[0][0]] < min(rank[board[0][0]], rank[board[1][0]], rank[board[2][0]], rank[board[3][0]]): #if we have the lowest pair
                    return "DISCARD:" + myHand[0] + '\n'
                else:
                    return "CHECK\n"
            elif myHand[0][0] in [board[0][0], board[1][0], board[2][0], board[3][0]] and myHand[1][0] in [board[0][0], board[1][0], board[2][0], board[3][0]]: #both cards used
                return "CHECK\n"
            else:
                if myHand[0][0] in [board[0][0], board[1][0], board[2][0], board[3][0]]:
                    return "DISCARD:" + myHand[1] + '\n' 
                else:
                    return "DISCARD:" + myHand[0] + '\n'
        
        if value.is_of_a_kind(combined)[0] == 1: #pair
            if myHand[0][0] == myHand[1][0]: #pockets
                return "CHECK\n"
            elif myHand[0][0] in [board[0][0], board[1][0], board[2][0], board[3][0]]:
                if rank[myHand[1][0]] < rank['J']:
                    return "DISCARD:" + myHand[1] + '\n' 
                else:
                    return "CHECK\n"
            elif myHand[1][0] in [board[0][0], board[1][0], board[2][0], board[3][0]]:
                if rank[myHand[0][0]] < rank['J']:
                    return "DISCARD:" + myHand[0] + '\n' 
                else:
                    return "CHECK\n"
            elif rank[myHand[0][0]] > rank[myHand[1][0]]: #discard lower card
                return "DISCARD:" + myHand[1] + '\n'
            else:
                return "DISCARD:" + myHand[0] + '\n'
        
        if rank[myHand[0][0]] > rank[myHand[1][0]]: #discard lower card
            return "DISCARD:" + myHand[1] + '\n'
        else:
            return "DISCARD:" + myHand[0] + '\n'
            
        return "CALL\n"
    
    else:
        return "CALL\n"
        limit = 0
        
        hand = value.get_full_hand(data, myHand)
        royal_check = value.is_royal(hand)
        full_value = value.is_full_house(hand)
        pair_value = value.is_of_a_kind(hand)
        flush_value = value.is_flush(hand)
        straight_value = value.is_straight(hand)
        high_value = value.high(hand)
        
        '''
        if royal_check[0] == 9 or royal_check[0] == 8 or pair_value[0] == 7 or full_value[0] == 6 or flush_value[0] == 5 or straight_value[0] == 4:
            return "RAISE:200\n" #Define what is meant by "lead in"
        if pair_value[0] == 3 or full_value[0] == 2: #Triple or Two Pair
            return "RAISE:200\n"
        '''
        
        
        if pair_value[0] == 1: #Pair
            if value.count_same_suit(boardCards)[0] == 3 or value.double_sided_straight(boardCards) != False:
                limit = limit*.75
            pair_card = value.is_of_a_kind(hand)[1]
            rank = 1
            for i in boardCards:
                if pair_card < i:
                    rank += 1
            limit = min(6*pair_card + (4-rank)*50, 200)
        else:
            limit = 20
        if high_value[0] == 0: #High Card
            limit = (5 + value.high(hand)[1])*2
        
        
        
        if value.count_same_suit(combined)[0] == 4:
            if value.count_same_suit(combined)[1] == suit[0] and value.count_same_suit(combined)[1] == suit[1]:
                limit = 60
            elif value.count_same_suit(combined)[1] == suit[0] or value.count_same_suit(combined)[1] == suit[1]:
                if value.high(combined)[1] >= 13:
                    limit = 120
                elif value.high(combined)[1] >= 9 and value.high(combined)[1] <=12:
                    limit = 80
                else:
                    limit = 30
    
    
    
        if value.double_sided_straight(combined) != False:
            limit = 100     
        if value.hole_straight(combined) != False:
            limit = 60
        
        
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
                    if canDoThis("CHECK\n", data):
                        return "CHECK\n"
                    return "FOLD\n"
                return "CALL\n"
        
            if packet[i][0:len("CHECK")] == "CHECK":
                return "CHECK\n"
            
        return "CHECK\n";
    
                
    