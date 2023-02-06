import random
import timeit

N = 9 #taille du sudoku
starttimer = [12, 0.0, 0.4] #[temps, temps_depart, temps_max]

def sudoku_generator(size): #génère un sudoku de taille size
    grid = [[0 for x in range(size)] for y in range(size)]
    return grid

def CheckValid(Grid,row,col,num):
    valid = True
    #vérifie que le nombre est valide dans la ligne
    for x in range(9):
        if (Grid[x][col] == num):
            valid = False
    #vérifie que le nombre est valide dans la colonne
    for y in range(9):
        if (Grid[row][y] == num):
            valid = False
    #vérifie que le nombre est valide dans le carré
    rowsection = row // 3
    colsection = col // 3
    for x in range(3):
        for y in range(3):
            if(Grid[rowsection*3 + x][colsection*3 + y] == num):
                valid = False
    #retourne vrai si le nombre est valide
    return valid

def MakeSudoku():
    #génère un sudoku vide
    Grid = [[0 for x in range(9)] for y in range(9)]      
    #mets des nombres aléatoires dans la grille
    for i in range(17):
        row = random.randrange(9)
        col = random.randrange(9)
        num = random.randrange(1,10)
        #vérifie que le nombre est valide
        while(not CheckValid(Grid,row,col,num) or Grid[row][col] != 0):
            row = random.randrange(9)
            col = random.randrange(9)
            num = random.randrange(1,10)
        Grid[row][col]= num;
    return Grid

def solution(grid, row, col):
    #créé une grille avec la solution et la retourne si elle existe
    sol=sudoku_generator(9)
    for i in range (9):
        for j in range(9):
            sol[i][j]=grid[i][j]
    if solveSudoku(sol, row, col):
        return sol
    else:
        return False

def solveSudoku(grid, row, col, tps=0.5): #vérifie la validité de la grille et la résoud si elle est valide
    #démarre un timer
    if starttimer[0] == 12 or row == col == 0:
        starttimer[0] = timeit.default_timer()
    starttimer[1] = timeit.default_timer()
    #si on arrive à la fin: return True
    if (row == N - 1 and col == N):
        return True
    if col == N:
        row += 1
        col = 0
    #si le temps est dépassé: return False
    if (starttimer[1] - starttimer[0]) > tps:
        return False
    #appel récursif
    if grid[row][col] > 0:
        return solveSudoku(grid, row, col + 1)
    #vérifie la validité du nombre
    for num in range(1, N + 1, 1):
        if CheckValid(grid, row, col, num):
            grid[row][col] = num
            if solveSudoku(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False

def grille_joueur(difficulte: int): #génère une grille joueur de difficulté en paramètre
    grid = solution(MakeSudoku(),0,0)
    while grid == False:
        grid = solution(MakeSudoku(),0,0)
    dif = difficulte
    grid_j = sudoku_generator(9)
    #génère une grille et sa solution, copie la solution dans la grille joueur et enlève des nombres aléatoires
    for i in range(9):
        for j in range(9):
            grid_j[i][j] = grid[i][j]
    while dif > 0:
        row = random.randrange(9)
        column = random.randrange(9)
        if grid_j[row][column] != 0:
            grid_j[row][column] = 0
            dif -= 1
    return grid_j