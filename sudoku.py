import os, time


def solve(puzzle, neighbors):
   ''' suggestion:
   # q_table is quantity table {'1': number of value '1' occurred, ...}
   variables, puzzle, q_table = initialize_ds(puzzle, neighbors)
   return recursive_backtracking(puzzle, variables, neighbors, q_table)
   '''
   variables = initial_variables(puzzle, neighbors)
   return recursive_backtracking(puzzle, variables, neighbors)


def sudoku_neighbors(csp_table):
   # each position p has its neighbors {p:[positions in same row/col/subblock], ...}
   neighbors = {}
   for x in range(0, 81):
      temp, temp2 = [], []
      for y in csp_table:
         if x in y:
            for z in y:
               temp.append(z)
      temp.remove(x)
      [temp2.append(y) for y in temp if y not in temp2]
      neighbors[x] = temp2
   return neighbors


def sudoku_csp(n=9):
   csp_table = [[k for k in range(i * n, (i + 1) * n)] for i in range(n)]  # rows
   csp_table += [[k for k in range(i, n * n, n)] for i in range(n)]  # cols
   temp = [0, 1, 2, 9, 10, 11, 18, 19, 20]
   csp_table += [[i + k for k in temp] for i in [0, 3, 6, 27, 30, 33, 54, 57, 60]]  # sub_blocks
   return csp_table


def checksum(solution):
   return sum([ord(c) for c in solution]) - 48 * 81  # One easy way to check a valid solution


def select_unassigned_var(assignment, variables):  # mrv
   min, var = 10, -1
   for x in variables:
      if assignment[x] == '.':
         if len(variables[x]) < min: min, var = len(variables[x]), x
   return var


def isValid(value, var_index, assignment, csp_table):
   for x in csp_table[var_index]:
      if value == assignment[x]: return False
   return True


def backtracking_search(puzzle, variables, csp_table):
   return recursive_backtracking(puzzle, variables, csp_table)


def recursive_backtracking(assignment, variables, csp_table):  # neighbor check_complete, select_unassigned_var, ordered_domain, isValid, and update_variables
   if assignment.find('.') == -1: return assignment #End case if puzzle completed
   var = select_unassigned_var(assignment, variables) #Select unassigned
   if var == -1: return None #End case if there is no results
   list = variables.pop(var)
   temp = []+list
   copy = {}
   while temp != []:
      val = temp.pop()
      for x, y in variables.items():
         copy[x] = y[:]
      if isValid(val, var, assignment, csp_table):
         for x in csp_table[var]:
            if x in copy:
               if val in copy[x]: copy[x].remove(val)
         tempassignment = f"{assignment[:var]}{val}{assignment[var + 1:]}"
         result = recursive_backtracking(tempassignment, copy, csp_table)
         if result != None: return result
         variables[var] = list
   return None


def initial_variables(puzzle, csp_table):
   sudoku = {}
   for x in range(81):
      sudoku[x] = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
   for x in range(81):
      for y in csp_table[x]:
         if puzzle[x] in sudoku[y]:
            sudoku[y].remove(puzzle[x])
   return sudoku


def main():
   filename = input("file name: ")
   if not os.path.isfile(filename):
      filename = "puzzles.txt"
   csp_table = sudoku_csp()  # rows, cols, and sub_blocks
   neighbors = sudoku_neighbors(
      csp_table)  # each position p has its neighbors {p:[positions in same row/col/subblock], ...}
   start_time = time.time()
   for line, puzzle in enumerate(open(filename).readlines()):
      #if line == 50: break  # check point: goal is less than 0.5 sec
      line, puzzle = line + 1, puzzle.rstrip()
      print("Line {}: {}".format(line, puzzle))
      solution = solve(puzzle, neighbors)
      if solution == None:
         print("No solution found.");
      else:
         print("{}({}, {})".format(" " * (len(str(line)) + 1), checksum(solution), solution))
   print("Duration:", (time.time() - start_time))


if __name__ == '__main__': main()
