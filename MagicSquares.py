#  File: MagicSquares.py
#  Description: HW 13 Solution
#  Student's Name: Daniel Carlson
#  Student's UT EID: djc3839
#  Course Name: CS 303E 
#  Unique Number: 50180
#
#  Date Created: 4/23/2020
#  Date Last Modified: 4/23/2020

class MagicSquare:
    def __init__(self,side):
        global grid
        self.side = side
        grid = [[0 for x in range(side)] for y in range(side)]      #Grid Population
        n = side
        i = 1                                                       #initialize i
        x = int((n-1)/2)                                            #set grid position
        y = 0
        grid[y][x] = i                                              #insert i into grid pos
        while i != (n**2):                                          #finish for i = n**2
            if i%n == 0:                                                #i multiple of n
                y += 1                                                      #move down
                if y > n-1:                                             #wrap y
                    y = 0
            else:                                                   #otherwise
                x += 1                                                  #move right
                if x > n-1:                                                 #wrap x
                    x = 0
                y -= 1                                                  #move up
                if y < 0:                                                   #wrap y
                    y = n-1
            i += 1                                                  #increment i
            grid[y][x] = i                                          #replace index with i

    def display():
        global grid
        print('\n'.join(''.join('{:5}'.format(i) for i in x) for x in grid))
        print("")

def main():
    num = 1
    while num <=13:
        print("Magic Square of size", num)
        print("")
        MagicSquare(num)
        MagicSquare.display()
        num += 2

main()
