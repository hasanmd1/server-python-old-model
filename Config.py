#!/usr/bin/python 3.10

''' Created by
Md Zahid Hasan '''

SERVER_CONFIRMATION = ''                                    #<16-bit number in decimal notation>\a\b
                                                            #Message with confirmation code. Can contain maximally 5 digits and the termination sequence \a\b.
SERVER_MOVE = '102 MOVE\a\b'.encode('utf-8')	            #102 MOVE\a\b
                                                            #Command to move one position forward
SERVER_TURN_LEFT = '103 TURN LEFT\a\b'.encode('utf-8')	    #103 TURN LEFT\a\b
                                                            #Command to turn left
SERVER_TURN_RIGHT = '104 TURN RIGHT\a\b'.encode('utf-8')    #104 TURN RIGHT\a\b
                                                            #Command to turn right
SERVER_PICK_UP = '105 GET MESSAGE\a\b'.encode('utf-8')	    #105 GET MESSAGE\a\b
                                                            #Command to pick up the message
SERVER_LOGOUT = '106 LOGOUT\a\b'.encode('utf-8')	        #106 LOGOUT\a\b
                                                            #Command to terminate the connection after successfull message discovery
SERVER_KEY_REQUEST = '107 KEY REQUEST\a\b'.encode('utf-8')  #Command to request Key ID for the communication
                                                            #107 KEY REQUEST\a\b
SERVER_OK = '200 OK\a\b'.encode('utf-8')	                #200 OK\a\b
                                                            #Positive acknowledgement
SERVER_LOGIN_FAILED = '300 LOGIN FAILED\a\b'.encode('utf-8')	#300 LOGIN FAILED\a\b
                                                                #Autentication failed
SERVER_SYNTAX_ERROR = '301 SYNTAX ERROR\a\b'.encode('utf-8')	#301 SYNTAX ERROR\a\b
                                                                #Incorrect syntax of the message
SERVER_LOGIC_ERROR = '302 LOGIC ERROR\a\b'.encode('utf-8')      #302 LOGIC ERROR\a\b
                                                                #Message sent in wrong situation

SERVER_KEY_OUT_OF_RANGE_ERROR = '303 KEY OUT OF RANGE\a\b'.encode('utf-8')  #Key ID is not in the expected range
                                                                            #303 KEY OUT OF RANGE\a\b
CLIENT_RECHARGING = 'RECHARGING\a\b'    #RECHARGING\a\b
                                        #Robot starts charging and stops to respond to messages.		12
CLIENT_FULL_POWER = 'FULL POWER\a\b'	#	FULL POWER\a\b
                                        #Robot has recharged and accepts commands again.

#declaring the length of different client related messages
CLIENT_USERNAME_LEN = 20
CLIENT_KEY_ID_LEN = 5
CLIENT_CONFIRMATION_LEN = 7
CLIENT_OK_LEN = 12
CLIENT_RECHARGING_LEN = 12
CLIENT_FULL_POWER_LEN = 12
CLIENT_MESSAGE_LEN = 100

#declaring Server's and client's pairs of authentication keys
Server_key = [23019, 32037, 18789, 16443, 18189]
Client_key = [32037, 29295, 13603, 29533, 21952]

#declaring the movements of the robot
Unintialized = -1
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
#These are the special symbols only used for just in case
special_character = ""
numeric_value = "0123456789"
ab = "\a\b"
