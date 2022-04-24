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


import socket
import sys

import threading
from asyncio import threads

from self import *
from time import sleep
from tcp_server import *


def main():
    #declaring my server
    my_server = tcp_Server()
    #declaring socket details
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #declaring server address and port number
    server_address = ('192.168.56.1', 6262)
    print('starting up on {} port {}'.format(*server_address))
    # binding socket to the port 6262
    mysock.bind(server_address)

    #listening to the incoming connections(10)
    mysock.listen(10)

    #communicating with the server
    my_server.Communication_With_Server(mysock)

#This is just used for the main
if __name__ == "__main__":
    main()


#!/usr/bin/python 3.10

import robot
import tcp_server
from Config import *
from tcp_server import *


def checker(data, connection, stage, treasureMessage, key, myHash):
    if data[len(data) - 1] != '\b' and data[len(data) - 2] != '\a':
        if stage == 0:
            if len(data) > CLIENT_USERNAME_LEN:
                tcp_server.tcp_Server.temporaryData, cnt = tcp_server.Collecting_Usable_Data(data, connection, stage, treasureMessage)
                if cnt >= 1:
                    return False
            return len(data) >= CLIENT_USERNAME_LEN
        if stage == 3 and treasureMessage:
            return len(data) >= CLIENT_MESSAGE_LEN

    return False


def Collecting_Usable_Data(RawData, connection, stage, treasureMessage):
    RawData = RawData.decode('utf-8')
    data = ''
    if RawData == '':
        return data, 0
    #print('', len(DataWithAdditionalStuff))
    counter = 0
    while RawData[len(RawData) - 2] != '\a' or RawData[
        len(RawData) - 1] != '\b':
        if '\a\b' not in RawData and not Validating_Length(RawData, stage,
                                                                         treasureMessage):
            return RawData, 0
        if '\0' in RawData:
            break
        connection.settimeout(1)
        tmp = connection.recv(1024)
        tmp = tmp.decode('utf-8')
        RawData += tmp
    if RawData[len(RawData) - 2] != '\a' or RawData[
        len(RawData) - 1] != '\b':
        return 'no', 0
    '''if any(x == '\a' or x == '\b' for x in DataWithAdditionalStuff) or (len(DataWithAdditionalStuff) > CLIENT_USERNAME_LEN and treasureMessage == False):

        return ['Usernamelengthcrossed'], 1'''

    while True:

        if RawData[counter] == '\a' and RawData[counter + 1] == '\b':
            if counter == len(RawData) - 2:
                # print('', DataWithAdditionalStuff[counter])
                return data, 0
            else:  # multiple messages
                data = [data]
                anotherData = ''
                counter += 2
                while True:
                    if RawData[counter] == '\a' and RawData[counter + 1] == '\b':
                        if counter == len(RawData) - 2:
                            data.append(anotherData)
                            return data, len(data)
                        else:
                            data.append(anotherData)
                            counter += 2
                            anotherData = ''
                    else:
                        anotherData += RawData[counter]
                        counter += 1

        else:
            data += RawData[counter]
            counter += 1

        # print('', data)


def Encode_Message(data):
    data = str(data)
    data += '\a\b'
    data = data.encode('utf-8')
    return data


def Server_Confirmation(name, Id):
    mySum = 0
    for myChar in name:
        mySum += ord(myChar)

    mySum *= 1000
    myHash = mySum % 65536
    mySum += Server_key[Id]
    mySum %= 65536
    mySum = Encode_Message(mySum)
    return mySum, myHash


def Hash_Comparision(number, hash, Id):
    number += 65536 - Client_key[Id]
    number %= 65536
    if number == hash:
        return True
    return False


def Coordinate_Extraction(data):
    x = 0
    y = 0
    tmp = data.split(' ')
    x = int(tmp[1])
    y = int(tmp[2])
    return x, y


def Validating_Length(data, stage, treasureMessage):
    myLen = len(data)
    if myLen and data[myLen - 1] == '\a':
        myLen -= 1
    if 'RECHARGING' in data or 'FULL POWER' in data:
        return myLen <= CLIENT_RECHARGING_LEN

    if stage == 2:
        return myLen <= CLIENT_CONFIRMATION_LEN
    else:
        if data == '':
            return True
        if stage == 0:
            return myLen <= CLIENT_USERNAME_LEN
        if stage == 1:
            return myLen <= CLIENT_KEY_ID_LEN
        if stage == 3 and not treasureMessage:
            return myLen <= CLIENT_OK_LEN
        return myLen <= CLIENT_MESSAGE_LEN


def Length_Text_Check(data, stage, treasureMessage):
    if 'RECHARGING' in data or 'FULL POWER' in data:
        return len(data) <= CLIENT_RECHARGING_LEN
    if stage == 0:
        return len(data) <= CLIENT_USERNAME_LEN
    if stage == 2:
        if len(data) <= CLIENT_CONFIRMATION_LEN:
            return not (' ' in data)
        return len(data) <= CLIENT_CONFIRMATION_LEN
    else:
        if data == '':
            return True
        if stage == 0:
            return len(data) <= CLIENT_USERNAME_LEN
        if stage == 1:
            if '\0' in data:
                return False
            return len(data) <= CLIENT_KEY_ID_LEN
        if stage == 3 and not treasureMessage:
            if len(data) <= CLIENT_OK_LEN:
                try:
                    if not (data[0] == 'O' and data[1] == 'K' and data[2] == ' '):
                        return False
                    tmp = data.split(' ')
                    tmp[1] = int(tmp[1])
                    tmp[2] = int(tmp[2])
                    a = tmp[0] + ' ' + str(tmp[1]) + ' ' + str(tmp[2])
                    if a != data:
                        return False
                except Exception as ex:
                    return False
            return len(data) <= CLIENT_OK_LEN
        return len(data) <= CLIENT_MESSAGE_LEN



#!/usr/bin/python

import threading
import logging
import os
import _thread
from curses.ascii import isdigit

import Helper_function
from Config import special_character
from Helper_function import *
from Helper_function import Collecting_Usable_Data
from robot import Robot
import socket
from threading import *


class New_Thread(threading.Thread):
    # This class is responsible for creating and implementing new threads

    def __init__(self):
        # constructor for handling threading
        threading.Thread.__init__(self)
        print("creating a thread:")

    def run(self):
        # Method dictating the executing path of the thread
        # threading.Thread.run(threading.Thread.__init__(self))
        print("executing the thread:")


class tcp_Server:
    def __init__(self):
        self.Thread_list = []

    def Communication_With_Server(self, mysock):
        count = 0
        while True:
            # Waiting for new connections
            print('[Starting Up the connections]...')
            New_connection, client_address = mysock.accept()
            count = count + 1
            New_connection.settimeout(1)
            # Initiating a new thread
            t1 = Thread(target=self.SingleThread_Communication, args=(mysock, New_connection, client_address))
            t1.start()

            if count == 0:
                self.__init__()
            else:
                # If a new thread--- store it in the list
                self.Thread_list.append(t1)
            # This is just for printing the clients connected with thread
            for x in self.Thread_list:
                print("", client_address)

    def SingleThread_Communication(self, mySocket, New_connection, client_address):
        myHash = 0
        step = 0
        recharge = False
        multiple_messages = False
        robot = Robot()
        data = ''
        username = ''
        key = 0
        counter = 0
        cnt = 0
        movecounter = 0
        try:
            print('[Receiving connection from]...', client_address)

            # Receiving the data
            while True:
                # For a single line message
                if not multiple_messages:
                    data = New_connection.recv(1024)
                    print('Received{!r}'.format(data))
                    # Avoiding syntax_pitfall
                    if data[len(data) - 1] != '\b' and data[len(data) - 2] != '\a' and Helper_function.checker(data,
                                                                                                               New_connection,
                                                                                                               step,
                                                                                                               robot.SecretMessage,
                                                                                                               key,
                                                                                                               myHash) == 1:
                        New_connection.sendall(SERVER_SYNTAX_ERROR)
                        # print('ss',data[len(data)-2], stage, robot.previouslyPickedUpTreasure)
                        break
                        # breaking down raw data to usable data
                    temp_storage, cnt = Collecting_Usable_Data(data, New_connection, step,
                                                               robot.SecretMessage)
                    # print('', temp_storage)

                if cnt:
                    # handling multiple message
                    multiple_messages = True
                    data = temp_storage[counter]
                    counter += 1
                    cnt -= 1
                    if not cnt:
                        counter = 0
                        multiple_messages = False
                else:
                    data = temp_storage
                    # handling different cases
                    if data == 'RECHARGING':
                        New_connection.settimeout(5)
                        recharge = True
                        continue
                    if data == 'FULL POWER':
                        recharge = False
                        New_connection.settimeout(1)
                        continue

                    if data == SERVER_LOGIN_FAILED:
                        New_connection.sendall(SERVER_LOGIN_FAILED)
                        break
                    if data == SERVER_SYNTAX_ERROR or not Length_Text_Check(data, step,
                                                                            robot.SecretMessage):
                        New_connection.sendall(SERVER_SYNTAX_ERROR)
                        break
                    if recharge:
                        New_connection.sendall(SERVER_LOGIC_ERROR)
                        break
                    if data == 'RECHARGING':
                        New_connection.settimeout(5)
                        recharge = True
                        continue
                    if data == 'FULL POWER':
                        recharge = False
                        New_connection.settimeout(1)
                        continue

                    if recharge:
                        New_connection.sendall(SERVER_LOGIC_ERROR)
                        break
                # using the step of the executing and handling the executing accordingly
                if step == 0:
                    # SERVER_KEY_REQUEST, Id = Key_authenticator(data1)
                    username = data
                    # used to look for unual/non-alphaneumeric letters
                    if any(x in special_character for x in data) and robot.SecretMessage == False:
                        New_connection.sendall(SERVER_SYNTAX_ERROR)
                        break
                    # print('x', data)
                    # useless code for now
                    elif username == 'error':
                        New_connection.sendall(SERVER_LOGIN_FAILED)
                        break
                    # useless code for now
                    elif username == 'Usernamelengthcrossed':
                        New_connection.sendall(SERVER_SYNTAX_ERROR)
                        break
                    else:
                        New_connection.sendall(SERVER_KEY_REQUEST)
                    step += 1
                elif step == 1:

                    if any(x not in numeric_value for x in data):
                        New_connection.sendall(SERVER_SYNTAX_ERROR)
                        break
                    key = int(data)
                    if (key < 0 or key > 4):
                        New_connection.sendall(SERVER_KEY_OUT_OF_RANGE_ERROR)
                        break

                    elif any(x in special_character for x in data):
                        New_connection.sendall(SERVER_SYNTAX_ERROR)
                        break
                    elif username == 'error':
                        New_connection.sendall(SERVER_LOGIN_FAILED)
                        break
                    else:
                        SERVER_CONFIRMATION, myHash = Server_Confirmation(username, int(data))
                        New_connection.sendall(SERVER_CONFIRMATION)
                        step += 1
                    # print('', key)
                elif step == 2:
                    if Hash_Comparision(int(data), myHash, key):
                        # print('', myHash)
                        New_connection.sendall(SERVER_OK)
                        # connection.sendall(robot.Move(99999999999, 99999999999))
                        New_connection.sendall(robot.FirstMove())
                        movecounter += 1
                        step += 1
                    elif int(data) > 99999:
                        New_connection.sendall(SERVER_SYNTAX_ERROR)
                    else:
                        New_connection.sendall(SERVER_LOGIN_FAILED)
                        break
                elif step == 3:

                    if data != '' and data[0] == 'O' and data[1] == 'K' and data[2] == ' ':
                        x, y = Coordinate_Extraction(data)
                        # print('', x, y)
                        # robot.Move(x, y)
                        New_connection.sendall(robot.Movement(x, y, movecounter))
                        movecounter += 1
                        # print('', robot.mycoordinate)
                        # print('', robot.mypreviouscoordinates)
                    else:
                        if data == '':
                            # print('0-1')
                            New_connection.sendall(
                                robot.Movement(robot.previousCoordinates[0], robot.previousCoordinates[1], movecounter))
                        else:
                            # print('0-2')
                            New_connection.sendall(SERVER_LOGOUT)
                            break
                    '''if data != '' and data[0] == 'O' and data[1] == 'K' and data[2] == ' ' and prevoiusx == x and previousy == y
                    elif data != '' and data[0] == 'O' and data[1] == 'K' and data[2] == ' ':
                        x, y = ExtractCoordinates(data)
                        connection.sendall(robot.Move(x, y, obstaclesfaced, moved))
                        prevoiusx = x
                        previousy = y

                    else:
                        if data == '':
                            connection.sendall(
                                robot.Move(robot.previousCoordinates[0], robot.previousCoordinates[1]))
                        else:
                            connection.sendall(SERVER_LOGOUT)
                            break'''
        except socket.timeout:
            print('Caught timeout')

        finally:
            # closing the connection && cleaning up the previous connection
            New_connection.close()



from tcp_server import *
from multiprocessing import connection

from tcp_server import *
from Helper_function import *
from Config import *


class Robot:
    def __init__(self):
        self.directionx = Unintialized
        self.directiony = Unintialized
        self.destinationdirectionx = Unintialized
        self.destinationdirectiony = Unintialized
        self.previousCoordinates = None
        self.Coordinates = None
        self.mydestinationdirection = None
        self.mycoordinate = None
        self.mypreviouscoordinates = None
        self.obstaclesfaced = 0
        self.obstaclemode = 0
        self.moved = 0
        self.obstaclemoves = 0
        self.flag = 0
        self.mode = 0
        self.level = 0
        self.SecretMessage = False
        # self.SecretMessage = False

    '''def GotoTreasure(self, x, y):

        my_move = self.direction


        return 0

    def facedestdirectionx(self):
        while abs(self.direction-self.destinationdirection[0]) != 0:
            if self.direction - self.destinationdirection[0] < 0:
                connection.sendall(SERVER_TURN_LEFT)
                self.direction -= 1
            elif self.direction - self.destinationdirection[0] > 0:
                connection.sendall(SERVER_TURN_RIGHT)
                self.direction += 1
    def facedestdirectiony(self):
        while abs(self.direction-self.destinationdirection[1]) != 0:
            if self.direction - self.destinationdirection[1] < 0:
                connection.sendall(SERVER_TURN_RIGHT)
                self.direction -= 1
            elif self.direction - self.destinationdirection[0] > 0:
                connection.sendall(SERVER_TURN_LEFT)
                self.direction += 1

    def gotodestinationx(self, movedx):
        if self.mydestinationdirection[0] < 0:
            self.Coordinates[0] += 1
            connection.sendall(SERVER_MOVE)
            movedx = 1
        elif self.mydestinationdirection[0] > 0:
            self.Coordinates[0] -= 1
            connection.sendall(SERVER_MOVE)
            movedx = 1
        return

    def gotodestinationy(self):
        if self.mydestinationdirection[1] < 0:
            self.Coordinates[0] += 1
            connection.sendall(SERVER_MOVE)
            movedy = 1
        elif self.mydestinationdirection[1] > 0:
            self.Coordinates[0] -= 1
            connection.sendall(SERVER_MOVE)
            movedy = 1
        return

    def goto_destination(self, canbemoved, movedx, movedy, obstaclesfaced, x, y):
        if canbemoved > 0 and x == self.Coordinates[0] and y == self.Coordinates[1]:
            self.facedestdirectionx()
            if self.direction-self.destinationdirection[0] == 0:
                self.gotodestinationx(movedx)

            if x == 0 :
                self.facedestdirectiony()
                if self.direction - self.destinationdirection[1] == 0:
                    self.gotodestinationy(movedy)

        elif movedx == 1 and x != self.Coordinates[0] and y != self.Coordinates[1]:
            obstaclesfaced += 1

            self.Coordinates[0] = x
            self.Coordinates[1] = y
            self.direction += 1
            connection.sendall(SERVER_TURN_RIGHT)
            self.Coordinates[1] = y + 1
            connection.sendall(SERVER_MOVE)
            self.direction -= 1
            connection.sendall(SERVER_TURN_LEFT)

            if self.direction == self.destinationdirection[0]:
                movedx = 0

        elif movedy == 1 and x != self.Coordinates[0] and y != self.Coordinates[1]:
            obstaclesfaced += 1
            movedy = 0
            self.Coordinates[0] = x
            self.Coordinates[1] = y
            self.direction += 1
            connection.sendall(SERVER_TURN_LEFT)
            self.Coordinates[0] = x + 1
            connection.sendall(SERVER_MOVE)
            self.direction -= 1
            connection.sendall(SERVER_TURN_RIGHT)

            if self.direction != self.destinationdirection[1]:
                movedy = 0'''

    def FirstMove(self):

        return SERVER_MOVE

    def Facedestinationdirection(self, moved):
        if self.Coordinates[0] != self.previousCoordinates[0] and self.Coordinates[1] != self.previousCoordinates[1]:
            if self.directionx == Unintialized:
                self.directionx = self.directiony
            if self.destinationdirectionx == Unintialized:
                self.destinationdirectionx = self.directiony
            if self.level == 0:
                self.level += 1
            if self.level == 2:
                self.level -= 1
            if self.directionx - self.destinationdirectionx < 0:
                self.directionx += 1
                self.directionx %= 4
                return SERVER_TURN_RIGHT
            if self.directionx - self.destinationdirectionx > 0:
                self.directionx += 3
                self.directionx %= 4
                return SERVER_TURN_LEFT
            if self.directionx - self.destinationdirectionx == 0 and self.mycoordinate[0] != 0:
                print('x')
                if self.destinationdirectionx == LEFT:
                    self.mycoordinate[0] -= 1
                else:
                    self.mycoordinate[0] += 1
                self.moved += 1
                if self.directiony == Unintialized:
                    self.directiony = self.directionx
                if self.destinationdirectiony == Unintialized:
                    self.destinationdirectiony = self.directionx
                return SERVER_MOVE
            if self.directionx - self.destinationdirectionx == 0 and self.mycoordinate[0] == 0:
                if self.level == 1:
                    self.level += 1
                if self.level == 0:
                    self.level += 2
                if self.directiony - self.destinationdirectiony < 0:
                    self.directiony += 1
                    self.directiony %= 4
                    print('y1', self.directiony, self.directionx)
                    return SERVER_TURN_RIGHT
                if self.directiony - self.destinationdirectiony > 0:
                    self.directiony += 3
                    self.directiony %= 4
                    return SERVER_TURN_LEFT
                if self.directiony - self.destinationdirectiony == 0 and self.mycoordinate[1] != 0:
                    print('y')
                    self.moved += 1
                    if self.destinationdirectiony == UP:
                        self.mycoordinate[1] += 1
                    else:
                        self.mycoordinate[1] -= 1
                    return SERVER_MOVE
                if self.directiony - self.destinationdirectiony == 0 and self.mycoordinate[1] == 0:
                    print('cx')
                    self.SecretMessage = True
                    return SERVER_PICK_UP
        if self.Coordinates[0] == self.previousCoordinates[0] and self.Coordinates[1] != self.previousCoordinates[1]:
            if self.level == 0:
                self.level += 2
            if self.level == 1:
                self.level += 1
            if self.directiony - self.destinationdirectiony < 0:
                self.directiony += 1
                self.directiony %= 4
                print('y1', self.directiony, self.directionx)
                return SERVER_TURN_RIGHT
            if self.directiony - self.destinationdirectiony > 0:
                self.directiony += 3
                self.directiony %= 4
                print('ap')
                return SERVER_TURN_LEFT
            if self.directiony - self.destinationdirectiony == 0 and self.mycoordinate[1] != 0:
                print('y')
                self.moved += 1
                if self.destinationdirectiony == UP:
                    self.mycoordinate[1] += 1
                else:
                    self.mycoordinate[1] -= 1
                if self.directionx == Unintialized:
                    self.directionx = self.directiony
                if self.destinationdirectionx == Unintialized:
                    self.destinationdirectionx = self.directiony
                return SERVER_MOVE
            if self.directiony - self.destinationdirectiony == 0 and self.mycoordinate[1] == 0:
                if self.level == 2:
                    self.level -= 1
                if self.level == 0:
                    self.level += 1
                if self.directionx - self.destinationdirectionx < 0:
                    self.directionx += 1
                    self.directionx %= 4
                    return SERVER_TURN_RIGHT
                if self.directionx - self.destinationdirectionx > 0:
                    self.directionx += 3
                    self.directionx %= 4
                    print('al')
                    return SERVER_TURN_LEFT
                if self.directionx - self.destinationdirectionx == 0 and self.mycoordinate[0] != 0:
                    print('x')
                    if self.destinationdirectionx == LEFT:
                        self.mycoordinate[0] -= 1
                    else:
                        self.mycoordinate[0] += 1
                    self.moved += 1
                    # self.directiony = self.directionx
                    return SERVER_MOVE
                if self.directionx - self.destinationdirectionx == 0 and self.mycoordinate[0] == 0:
                    print('cx')
                    self.SecretMessage = True
                    return SERVER_PICK_UP

        if self.Coordinates[0] != self.previousCoordinates[0] and self.Coordinates[1] == self.previousCoordinates[1]:
            if self.level == 0:
                self.level += 1
            if self.level == 2:
                self.level -= 1
            if self.directionx == Unintialized:
                self.directionx = self.directiony
            if self.destinationdirectionx == Unintialized:
                self.destinationdirectionx = self.directiony
            if self.directionx - self.destinationdirectionx < 0:
                self.directionx += 1
                self.directionx %= 4
                return SERVER_TURN_RIGHT
            if self.directionx - self.destinationdirectionx > 0:
                self.directionx += 3
                self.directionx %= 4
                print('ay')
                return SERVER_TURN_LEFT
            if self.directionx - self.destinationdirectionx == 0 and self.mycoordinate[0] != 0:
                print('x')
                if self.destinationdirectionx == LEFT:
                    self.mycoordinate[0] -= 1
                else:
                    self.mycoordinate[0] += 1
                self.moved += 1
                if self.directiony == Unintialized:
                    self.directiony = self.directionx
                if self.destinationdirectiony == Unintialized:
                    self.destinationdirectiony = self.directionx
                return SERVER_MOVE
            if self.directionx - self.destinationdirectionx == 0 and self.mycoordinate[0] == 0:
                if self.level == 1:
                    self.level += 1
                if self.level == 0:
                    self.level += 2
                if self.directiony - self.destinationdirectiony < 0:
                    self.directiony += 1
                    self.directiony %= 4
                    print('y1', self.directiony, self.directionx)
                    return SERVER_TURN_RIGHT
                if self.directiony - self.destinationdirectiony > 0:
                    self.directiony += 3
                    self.directiony %= 4
                    print('ax')
                    return SERVER_TURN_LEFT
                if self.directiony - self.destinationdirectiony == 0 and self.mycoordinate[1] != 0:
                    print('y')
                    self.moved += 1
                    if self.destinationdirectiony == UP:
                        self.mycoordinate[1] += 1
                    else:
                        self.mycoordinate[1] -= 1
                    return SERVER_MOVE
                if self.directiony - self.destinationdirectiony == 0 and self.mycoordinate[1] == 0:
                    self.SecretMessage = True
                    return SERVER_PICK_UP
        if self.mycoordinate[0] == 0 and self.mycoordinate[1] == 0:
            self.SecretMessage = True
            return SERVER_PICK_UP

    def Finddestinationdirection(self):
        if self.mydestinationdirection[0] > 0:
            self.destinationdirectionx = RIGHT
        elif self.mydestinationdirection[0] < 0:
            self.destinationdirectionx = LEFT
        if self.mydestinationdirection[1] > 0:
            self.destinationdirectiony = UP
        elif self.mydestinationdirection[1] < 0:
            self.destinationdirectiony = DOWN

        return 0

    def Finddirection(self, x, y):
        if x > self.previousCoordinates[0]:
            self.directionx = RIGHT
            # self.direction[0] = RIGHT
        elif x < self.previousCoordinates[0]:
            self.directionx = LEFT
            # self.direction[0] = LEFT
        if y < self.previousCoordinates[1]:
            self.directiony = DOWN
            # self.direction[1] = DOWN
        elif y > self.previousCoordinates[1]:
            self.directiony = UP
            # self.direction[1] = UP

        return 0

    def Obstaclemode(self):
        print('', self.mypreviouscoordinates)
        if self.mycoordinate[0] != 0 or self.mycoordinate[1] != 0:
            if self.level == 2:
                if self.obstaclemoves == 0:
                    self.mode += 1
                    self.obstaclemoves += 1
                    self.directiony += 1
                    self.directiony %= 4
                    return SERVER_TURN_RIGHT

                if self.obstaclemoves == 1:
                    self.obstaclemoves += 1
                    if self.directiony == RIGHT:
                        self.mycoordinate[0] += 1
                    else:
                        self.mycoordinate[0] -= 1
                    return SERVER_MOVE
                if self.obstaclemoves == 2:
                    self.obstaclemoves += 1
                    self.directiony += 3
                    self.directiony %= 4
                    return SERVER_TURN_LEFT

                if self.obstaclemoves == 3:
                    if self.mycoordinate[1] < 0:
                        self.mycoordinate[1] += 1
                    else:
                        self.mycoordinate[1] -= 1
                    if self.mycoordinate[1] == 0:
                        self.obstaclemoves += 2
                    else:
                        self.obstaclemoves += 1
                    return SERVER_MOVE

                if self.obstaclemoves == 4:
                    self.obstaclemoves += 1
                    if self.mycoordinate[1] < 0:
                        self.mycoordinate[1] += 1
                    else:
                        self.mycoordinate[1] -= 1
                    return SERVER_MOVE

                if self.obstaclemoves == 5:
                    self.directiony += 3
                    self.directiony %= 4
                    self.obstaclemoves += 1
                    return SERVER_TURN_LEFT
                if self.obstaclemoves == 6:
                    self.obstaclemoves += 1
                    if self.directiony == RIGHT:
                        self.mycoordinate[0] += 1
                    else:
                        self.mycoordinate[0] -= 1
                    return SERVER_MOVE
                if self.obstaclemoves == 7:
                    self.directiony += 1
                    self.directiony %= 4
                    self.obstaclemoves += 1
                    return SERVER_TURN_RIGHT
                if self.obstaclemoves == 8:
                    self.moved *= 0
                    self.mode *= 0
                    self.obstaclemoves -= 8

            if self.level == 1:
                print('gg')
                if self.obstaclemoves == 0:
                    self.mode += 2
                    self.obstaclemoves += 1
                    self.directionx += 1
                    self.directionx %= 4
                    return SERVER_TURN_RIGHT

                if self.obstaclemoves == 1:
                    self.obstaclemoves += 1
                    if self.directionx == UP:
                        self.mycoordinate[1] += 1
                    else:
                        self.mycoordinate[1] -= 1
                    return SERVER_MOVE
                if self.obstaclemoves == 2:
                    self.obstaclemoves += 1
                    self.directionx += 3
                    self.directionx %= 4
                    return SERVER_TURN_LEFT

                if self.obstaclemoves == 3:

                    if self.mycoordinate[0] < 0:
                        self.mycoordinate[0] += 1
                    else:
                        self.mycoordinate[0] -= 1
                    if self.mycoordinate[0] == 0:
                        self.obstaclemoves += 2
                    else:
                        self.obstaclemoves += 1
                    return SERVER_MOVE
                if self.obstaclemoves == 4:
                    self.obstaclemoves += 1
                    if self.mycoordinate[0] < 0:
                        self.mycoordinate[0] += 1
                    else:
                        self.mycoordinate[0] -= 1
                    return SERVER_MOVE

                if self.obstaclemoves == 5:
                    self.directionx += 3
                    self.directionx %= 4
                    self.obstaclemoves += 1
                    return SERVER_TURN_LEFT
                if self.obstaclemoves == 6:
                    self.obstaclemoves += 1
                    if self.directionx == UP:
                        self.mycoordinate[1] += 1
                    else:
                        self.mycoordinate[1] -= 1
                    return SERVER_MOVE
                if self.obstaclemoves == 7:
                    self.directionx += 1
                    self.directionx %= 4
                    self.obstaclemoves += 1
                    return SERVER_TURN_RIGHT
                if self.obstaclemoves == 8:
                    self.moved *= 0
                    self.obstaclemoves -= 8
        elif self.mycoordinate[0] == 0 and self.mycoordinate[1] != 0:
            if self.obstaclemoves == 0:
                self.obstaclemoves += 1
                self.directiony += 1
                self.directiony %= 4
                return SERVER_TURN_RIGHT

            if self.obstaclemoves == 1:
                self.obstaclemoves += 1
                if self.directiony == RIGHT:
                    self.mycoordinate[0] += 1
                else:
                    self.mycoordinate[0] -= 1
                return SERVER_MOVE
            if self.obstaclemoves == 2:
                self.obstaclemoves += 1
                self.directiony += 3
                self.directiony %= 4
                return SERVER_TURN_LEFT

            if self.obstaclemoves == 3 or self.obstaclemoves == 4:
                self.obstaclemoves += 1
                if self.mycoordinate[1] < 0:
                    self.mycoordinate[1] += 1
                else:
                    self.mycoordinate[1] -= 1
                return SERVER_MOVE

            if self.obstaclemoves == 5:
                self.directiony += 3
                self.directiony %= 4
                self.obstaclemoves += 1
                return SERVER_TURN_LEFT
            if self.obstaclemoves == 6:
                self.obstaclemoves += 1
                if self.directiony == RIGHT:
                    self.mycoordinate[0] += 1
                else:
                    self.mycoordinate[0] -= 1
                return SERVER_MOVE
            if self.obstaclemoves == 7:
                self.directiony += 1
                self.directiony %= 4
                self.obstaclemoves += 1
                return SERVER_TURN_RIGHT
            if self.obstaclemoves == 8:
                self.moved *= 0
                self.obstaclemoves -= 8
        elif self.mycoordinate[0] != 0 and self.mycoordinate[1] == 0:
            if self.obstaclemoves == 0:
                self.obstaclemoves += 1
                self.directionx += 1
                self.directionx %= 4
                return SERVER_TURN_RIGHT

            if self.obstaclemoves == 1:
                self.obstaclemoves += 1
                if self.directionx == UP:
                    self.mycoordinate[1] += 1
                else:
                    self.mycoordinate[1] -= 1
                return SERVER_MOVE
            if self.obstaclemoves == 2:
                self.obstaclemoves += 1
                self.directionx += 3
                self.directionx %= 4
                return SERVER_TURN_LEFT

            if self.obstaclemoves == 3 or self.obstaclemoves == 4:
                self.obstaclemoves += 1
                if self.mycoordinate[0] < 0:
                    self.mycoordinate[0] += 1
                else:
                    self.mycoordinate[0] -= 1
                return SERVER_MOVE

            if self.obstaclemoves == 5:
                self.directionx += 3
                self.directionx %= 4
                self.obstaclemoves += 1
                return SERVER_TURN_LEFT
            if self.obstaclemoves == 6:
                self.obstaclemoves += 1
                if self.directionx == UP:
                    self.mycoordinate[1] += 1
                else:
                    self.mycoordinate[1] -= 1
                return SERVER_MOVE
            if self.obstaclemoves == 7:
                self.directionx += 1
                self.directionx %= 4
                self.obstaclemoves += 1
                return SERVER_TURN_RIGHT
            if self.obstaclemoves == 8:
                self.moved *= 0
                self.obstaclemoves -= 8
        else:
            self.SecretMessage = True
            return SERVER_PICK_UP
        return 0

    def Movement(self, x, y, movecounter):

        print('', x, y, self.previousCoordinates, self.mycoordinate, self.Coordinates, self.directionx, self.directiony,
              self.destinationdirectionx, self.destinationdirectiony, self.mypreviouscoordinates)
        print('', self.moved)
        if self.previousCoordinates is None and self.directionx == Unintialized and self.directiony == Unintialized and movecounter == 1:
            self.previousCoordinates = [x, y]
            self.direction = Unintialized
            print('1')
            return SERVER_MOVE
        if self.directionx == Unintialized and self.directiony == Unintialized and self.previousCoordinates == [x,
                                                                                                                y] and movecounter > 1 and self.flag == 0:
            self.previousCoordinates = [x, y]
            self.direction = Unintialized
            #movecounter -= 1
            print('2')
            self.flag += 1
            return SERVER_TURN_RIGHT
        if self.directionx == Unintialized and self.directiony == Unintialized and self.previousCoordinates == [x,
                                                                                                                y] and movecounter > 1 and self.flag == 1:
            self.previousCoordinates = [x, y]
            self.direction = Unintialized
            movecounter -= 1
            print('2')
            self.flag *= 0
            return SERVER_MOVE

        if self.moved == 1:
            print('', self.mycoordinate)
            if (self.mycoordinate[0] != x or self.mycoordinate[1] != y and self.moved >= 0) or (
                    self.mycoordinate[0] == x and self.mycoordinate[1] == y and self.obstaclemoves > 0):
                self.obstaclesfaced += 1
                self.mycoordinate = self.mypreviouscoordinates
                print('v', self.mycoordinate)
                if self.obstaclemoves < 8:
                    print('v1', self.mypreviouscoordinates, self.mycoordinate)
                    return self.Obstaclemode()
                elif self.obstaclemoves == 8:
                    self.Obstaclemode()
            elif self.mycoordinate[0] == x and self.mycoordinate[1] == y and self.obstaclemoves == 0:
                self.moved *= 0
            elif self.mycoordinate[1] == 0 and self.mycoordinate[0] == 0:
                self.SecretMessage = True
                return SERVER_PICK_UP
            # print('', self.mypreviouscoordinates)
            # print('', self.mycoordinate)
            print('3')

        if self.moved == 0:
            self.mypreviouscoordinates = [x, y]
            print('c', self.mypreviouscoordinates)

        if self.previousCoordinates != None and self.previousCoordinates != [x, y] and (
                self.directionx == Unintialized or self.directiony == Unintialized) and self.moved == 0 and movecounter >= 2:
            if self.Coordinates == None:
                self.Coordinates = [x, y]
                self.mycoordinate = [x, y]
                self.Finddirection(x, y)
                self.mydestinationdirection = [0 - x, 0 - y]
                # self.mydestinationdirection[1] = 0 - y
                self.Finddestinationdirection()

            return self.Facedestinationdirection(self.moved)

        if self.directionx != Unintialized and self.directiony != Unintialized and self.moved == 0:
            return self.Facedestinationdirection(self.moved)

        print('', x, y, self.previousCoordinates, self.mycoordinate, self.Coordinates, self.directionx, self.directiony,
              self.destinationdirectionx, self.destinationdirectiony, self.mypreviouscoordinates)
        print('', self.moved)

