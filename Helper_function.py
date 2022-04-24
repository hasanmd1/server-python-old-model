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
