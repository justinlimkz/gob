import argparse
import socket
import sys

import preflop
import flop
import turn
import river
import value
import preflop_fold

"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""
class Player:
    def run(self, input_socket):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()
        foldHistory = []
        ourScore = 0

        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print ("Gameover, engine disconnected.")
                break

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.
            print (data)
            
            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!
            
            
            word = data.split()[0]
            handId = 0
                        
            if word == "NEWGAME":
                myName = data.split()[1]
                oppName = data.split()[2]
                
            if word == "NEWHAND":
                myHand = [data.split()[3], data.split()[4]]
                print (myHand)
                handId = int(data.split()[1])
                ourScore = int(data.split()[5])
                
            if word == "GETACTION":  
                numBoardCards = int(data.split()[2]) 
                if ourScore <= -2000:
                    return "CHECK\n"
                elif numBoardCards == 0:
                    if sum(foldHistory[-50:]) >= 40:
                        action = preflop_fold.getAction(myHand, data)
                    else:    
                        action = preflop.getAction(myHand, data)
                    
                elif numBoardCards == 3:
                    packet = data.split()
                    
                    numBoardCards = int(packet[2])
                    numLastActions = int(packet[2+numBoardCards+1])
                    
                    for i in range(2+numBoardCards+1+1, 2+numBoardCards+1+numLastActions+1):
                        if packet[i][0:len("DISCARD")] == "DISCARD":
                            discard = packet[i].split(":")
                            if len(discard) > 2:
                                if discard[1] == myHand[0]:
                                    myHand[0] = discard[2]
                                else:
                                    myHand[1] = discard[2]
                    action = flop.getAction(myHand, data)
                elif numBoardCards == 4:
                    packet = data.split()
                    
                    numBoardCards = int(packet[2])
                    numLastActions = int(packet[2+numBoardCards+1])
                    
                    for i in range(2+numBoardCards+1+1, 2+numBoardCards+1+numLastActions+1):
                        if packet[i][0:len("DISCARD")] == "DISCARD":
                            discard = packet[i].split(":")
                            if len(discard) > 2:
                                if discard[1] == myHand[0]:
                                    myHand[0] = discard[2]
                                else:
                                    myHand[1] = discard[2]
                    
                    action = turn.getAction(myHand, data)
                else:
                    action = river.getAction(myHand, data)
                s.send(action)
            elif word == "HANDOVER":
                foldAction = "FOLD:"+oppName
                if foldAction in data:
                    foldHistory += [1]
                else:
                    foldHistory += [0]
                
            elif word == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print ('Connecting to %s:%d' % (args.host, args.port))
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print ('Error connecting! Aborting')
        exit()

    bot = Player()
    bot.run(s)
