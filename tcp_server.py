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
