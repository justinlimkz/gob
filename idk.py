# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 17:32:38 2017

@author: Jeff
"""
def get_full_hand(data, newhand):
    x=data.split()
    y=newhand.split()
    hand=y[3:5]
    num_board=x[2]
    full_hand=hand+x[3:((int(num_board))+3)]
    return full_hand

def is_of_a_kind(hand):#for 2,3,4 of a kind
    list_cards=[]
    list_counts=[]
    card_dict={'A':14,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13}
    for i in hand:
        card=i[0]
        list_cards.append(card)
    for i in list_cards:
        count=0
        for j in list_cards:
            if i==j:
                count+=1
        list_counts.append(count)
    if 4 in list_counts:
        for i in range(5):
            if list_counts[i]==4:
                four=card_dict[list_cards[i]]
        return [7,four]
    if 3 in list_counts:
        for i in range(5):
            if list_counts[i]==3:
                three=card_dict[list_cards[i]]
        return [3,three]
    if 2 in list_counts:
        for i in range(5):
            if list_counts[i]==2:
                two=card_dict[list_cards[i]]
        return [1,two]
    else: 
        return [-1,-1]

def is_full_house(hand):#for full house or 2 pair
    list_cards=[]
    list_counts=[]
    twocount=0
    threecount=0
    current_max=0
    card_dict={'A':14,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13 }
    for i in hand:
        card=i[0]
        list_cards.append(card)
    for i in list_cards:
        count=0
        for j in list_cards:
            if i==j:
                count+=1
            if count==3:
                house=i
        list_counts.append(count)
    for i in list_counts:
        if i==2:
            twocount+=1
        if i==3:
            threecount+=1
    if 2 in list_counts:
        if 3 in list_counts:
            return [6,card_dict[house]]
        elif twocount>=4:
            for i in range(5):
                if list_counts[i]==2:
                    if card_dict[list_cards[i]]>current_max:
                        current_max=card_dict[list_cards[i]]
            return [2, current_max]
    elif threecount>=6:
        for i in range(5):
            if list_counts[i]==3:
                if card_dict[list_cards[i]]>current_max:
                    current_max=card_dict[list_cards[i]]
        return [6, current_max]
    return [-1,-1]

        
def is_flush(hand):
    list_suits=[]
    list_cards=[]
    flush=False
    count=0
    card_dict={'A':14,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13}
    for i in hand:
        suit=i[1]
        list_suits.append(suit)
        card=i[0]
        list_cards.append(card_dict[card])
    list_cards.sort()
    suits=['c','d','s','h']
    for i in suits:
        for suit in list_suits:
            if suit==i:
                count+=1
                if count>=5:
                    flush=True
    if flush:
        return [5,list_cards[4]]
    else:
        return [-1,-1]

def is_straight(hand):
    list_card=[]
    straight=False
    card_dict={'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13 }
    for i in hand:
        card=i[0]
        list_card.append(card_dict[card])
    list_card.sort()
    for i in range(len(hand)-4):
        counter=0
        for j in range(4):
            if list_card[i+j]==list_card[i+j+1]-1:
                counter+=1
            if counter==4:
                high=list_card[i+j+1]
                straight=True
                return [4,high]
    list_card_two=[]
    card_dict={'A':14,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13}
    for i in hand:
        card=i[0]
        list_card_two.append(card_dict[card])
    list_card_two.sort()
    for i in range(len(hand)-4):
        counter=0
        for j in range(4):
            if list_card[i+j]==list_card[i+j+1]-1:
                counter+=1
            if counter==4:
                high=list_card[i+j+1]
                straight=True
                return [4,high]
    if not straight:
        return [-1,-1]

def is_royal(hand):#for royal or straight flush
    if is_straight(hand)[0]==4 and is_flush(hand)[0]==5 and is_straight(hand)[1]==14:
        return [9,15]
    elif is_straight(hand)[0]==4 and is_flush(hand)[0]==5:
        return [8, is_flush(hand)[1]]
    else: 
        return [-1,-1]
        
def high(hand):#determines high card
    list_card=[]
    card_dict={'A':14,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13}
    for i in hand:
        splitted=i.split()
        card=splitted[0]
        list_card.append(card_dict[card])
    list_card.sort()
    return [0,list_card[4]]
    
new='NEWHAND 10 true Ah Ac 200 200 20.000000'
get='GETACTION 30 4 As Ks Qh Qd 3 CHECK:two CHECK:one DEAL:RIVER 2 CHECK BET:2:30 19.997999999999998'
print (get_full_hand(get,new))
