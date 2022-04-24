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
