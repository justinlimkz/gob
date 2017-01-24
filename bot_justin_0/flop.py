import value 

rank = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9 ,'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

NO = [-1, -1]

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
    combined = myHand
    print combined
    combined.extend(board)
    print board
    print combined
    
    if canDoThis("DISCARD", data):
        if value.is_flush(combined) != NO or value.is_straight(combined) != NO or value.is_full_house(combined) != NO or value.is_of_a_kind(combined)[0] == 7:
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
                if rank[myHand[0][0]] < min(rank(board[0][0]), rank(board[1][0]), rank(board[2][0])):
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
        
        return "CALL\n"
        
    else:
        return "CALL\n"