import pandas as pd
import numpy as np

#starting sudoku values
#sudoku = list('100000008060020070002807600050109080080000020010602050008501400020070090900000003')
#sudoku = list('500010007010000090020703040280507014000000000950601072090204030070000050600090001')
sudoku = list('613000000005603000090000016001004008408050902300700600120000070000309100000000829')
#sudoku = list('100090508006700000009851000000200804050000090201006000000167200000008900702040006')
for i in range(0, 81):
    sudoku[i] = int(sudoku[i])

all_options = set([1,2,3,4,5,6,7,8,9])

#make sudoku dataframe
columns = list('ABCDEFGHI')
rows = list('abcdefghi')
column_dic = {}
i = 0
for column in columns:
        column_dic['{}'.format(column)] = sudoku[i:i+9]
        i = i+9
df = pd.DataFrame(column_dic,index=rows)

#helper dictionary
not_it = {}
for column in columns:
    for row in rows:
        not_it['{}{}'.format(column,row)] = []

groups = {1:['Aa','Ba','Ca','Ab','Bb','Cb','Ac','Bc','Cc'],
         2:['Da','Ea','Fa','Db','Eb','Fb','Dc','Ec','Fc'],
         3:['Ga','Ha','Ia','Gb','Hb','Ib','Gc','Hc','Ic'],
         4:['Ad','Bd','Cd','Ae','Be','Ce','Af','Bf','Cf'],
         5:['Dd','Ed','Fd','De','Ee','Fe','Df','Ef','Ff'],
         6:['Gd','Hd','Id','Ge','He','Ie','Gf','Hf','If'],
         7:['Ag','Bg','Cg','Ah','Bh','Ch','Ai','Bi','Ci'],
         8:['Dg','Eg','Fg','Dh','Eh','Fh','Di','Ei','Fi'],
         9:['Gg','Hg','Ig','Gh','Hh','Ih','Gi','Hi','Ii']}

def whats_not_possible():
    for column in columns:
        for row in rows:
            # if element is already specified, add all other options to the not_it dictionary 
            if df[column][row] > 0:
                x = [1,2,3,4,5,6,7,8,9]
                x.remove(df[column][row])
                not_it['{}{}'.format(column,row)] = x
            # eliminate options that the element cannot be based on columns and rows
            else:
                x = list(set(list(df[column])+ list(df.loc[row])))
                x = [i for i in x if i != 0]
                not_it['{}{}'.format(column,row)] = x

#get numbers from group
def get_group_values(group_number): 
    result = []
    for element in groups[group_number]:
        value = df[element[0]][element[1]]
        if value == 0:
            pass
        else:
            result.append(value)
    return set(result)

def update_by_identification():
    for group in all_options:
        remaining_options = all_options - get_group_values(group)
        for option in remaining_options:
            #for all of the spaces in the group, check if each option is eliminated from all but one input. If so, add the input to the df
            potential = {}
            for element in groups[group]:
                if option in not_it[element]:
                    pass
                else:
                    potential[element] = option
            if len(potential) == 1:
                df[list(potential.keys())[0][0]][list(potential.keys())[0][1]] = option
            else: 
                pass
    whats_not_possible()
    progress.append(sum(df.sum()))
    print(sum(df.sum()))

def update_by_elimination():
    for element in not_it:
        if len(not_it[element]) < 8:
            pass
        else:
            df[element[0]][element[1]] = list(all_options - set(not_it[element]))[0]
    progress.append(sum(df.sum()))
    print('elimination')

def solve_sudoku():
    update_by_identification()
    update_by_identification()
    while sum(df.sum()) < 405:
        update_by_identification()
        if progress[-1] == progress[-2]:
            update_by_elimination()
        elif sum(df.sum()) == 405:
            break
    print(df)

progress = [sum(df.sum())]
solve_sudoku()
