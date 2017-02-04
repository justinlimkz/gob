import value

def evaluate(myHand, data):
    rank = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9 ,'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    NO = [-1, -1]

    packet = data.split()
    
    numBoardCards = int(packet[2])
    numLastActions = int(packet[2+numBoardCards+1])
    numLegalActions = int(packet[2+numBoardCards+1+numLastActions+1])
    
    num = [rank[myHand[0][0]], rank[myHand[1][0]]]
    suit = [myHand[0][1], myHand[1][1]]
    currentCards = packet[2:2+numBoardCards]
    
    board = packet[3:3+numBoardCards]
    combined = myHand+board
    
    if numBoardCards == 0:
        #if data.split()[4] == "POST:1:EzMoney" and abs(num[0]-num[1]) > 4 and suit[0] != suit[1] and max(num[0], num[1]) < 10:
            #limit = 0

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
                    
    elif numBoardCards == 3:    
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
                   
    elif numBoardCards == 4:      
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
            if myHand[0][0] in [board[0][0], board[1][0], board[2][0]]:
                limit = min(6*rank[myHand[0][0]]+(4-rank[myHand[0][0]]),100)
            elif myHand[0][0] in [board[0][0], board[1][0], board[2][0]]:
                limit = min(6*rank[myHand[1][0]]+(4-rank[myHand[1][0]]),100)
            else:
                limit = 10

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
            
    else:
        hand = combined
        boardCards = board
        if value.is_royal(hand) != NO or value.is_flush(hand) != NO or value.is_of_a_kind(hand)[0] == 7 or value.is_full_house(hand)[0] == 6 or value.is_straight(hand) != NO:
            limit = 200
        elif value.is_full_house(hand)[0]==2:
            if value.count_same_suit(boardCards)[0]==4 or value.double_sided_straight(boardCards)!=False:
                limit=25
            elif value.is_full_house(hand)[1] in myHand:
                limit = 200
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
            
    return limit