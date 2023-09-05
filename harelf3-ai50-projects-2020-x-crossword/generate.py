import sys


from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        """ print(self.crossword.variables)
        print(self.crossword.overlaps[Variable(1, 4, 'down', 4),Variable(4, 1, 'across', 4)])
        print(Variable(1, 4, 'down', 4).cells[3])
        print(Variable(4, 1, 'across', 4).cells[3]) """  
        """         
        self.consistent({(Variable(0, 1, 'down', 5)):"aaaaa", 
        (Variable(1, 4, 'down', 4)): "aaaa", 
        (Variable(0, 1, 'across', 3)):"aaa"}) """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # we want var length and to compare it to each domain length if different remove it 
        ###
        for var in self.crossword.variables:
            domain_copy = self.domains[var].copy()
            for domain in domain_copy:
                if var.length != len(domain):
                    self.domains[var].remove(domain)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        ###
        # we get its overlaping point 
        over_lap = self.crossword.overlaps[x,y]
        # if no over lap they have no binary constraints
        if  over_lap == None:
            return False
        revised = False
        
        # the cell number which is the same 
        xoverlap = over_lap[0]
        yoverlap = over_lap[1]
        xdomain_copy = self.domains[x].copy()
        # we check for every x domain if any y value satisfy if it satisfy it we continue if go all loop we remove it 
        for xdomain in xdomain_copy:
            count = 0 
            for ydomain in self.domains[y]:
                # this means that x is good for one domain which means we dont need to remove him 
                if xdomain[xoverlap] == ydomain[yoverlap]:
                    count = 1
                # else we say xdomain is bad not working here 
            if count == 0 :
                self.domains[x].remove(xdomain)
                revised =True
        return revised        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        ###
        # if they dont give us arcs back we will take all probleam arcs 
        if arcs == None:
            arcs =set()
            for variable in self.crossword.variables:
                for neighbor in self.crossword.neighbors(variable):
                    if (neighbor, variable) in arcs:
                        continue
                    arcs.add((variable ,neighbor))
        queue = arcs.copy()
        # while queue isnt empty
        ###
        while queue :
            x,y = queue.pop()
            # we run to see if this arc is consistant 
            if self.revise(x,y):
                # if not and x cannot take any domain we say this is currently unsolvabe
                if len(self.domains[x]) == 0:
                    return False
                # we want to check if all other arcs still good
                neighbors = self.crossword.neighbors(x)
                neighbors.remove(y)
                for var in neighbors:
                    queue.add((var,x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        ###
        # we check if assignement is empty id yes then it is not complete 
        if assignment== {}:
            return False
        # we check if they have the same amount of vars if no then false 
        if len(assignment) != len(self.crossword.variables):
            return False
        for value in assignment:
            if assignment[value] not in self.crossword.words:
                return False 
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # all values are distinct 
        ###
        # what does the fact that this is none means ?? 
        # if assignment == None:
        for var1 in assignment:
            for var2 in assignment:
                if var1 == var2:
                    continue
                if assignment[var1] == assignment[var2]:
                    return False
        # all values are current length 
        for var1 in assignment:
            if var1.length != len(assignment[var1]):
                return False
        # no conflicts with neighbors 
        for var1 in assignment: 
            neighbors = self.crossword.neighbors(var1)
            for neighbor in neighbors:
                over_lap = self.crossword.overlaps[var1,neighbor]
                x, y = over_lap
                # so we will catch the fact not all neighbors are in assignemet 
                if neighbor not in assignment:
                    continue
                if assignment[var1][x] != assignment[neighbor][y]:
                    return False
        return True
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        ###
        domains = self.domains[var]
        neighbors = self.crossword.neighbors(var)
        domains_dict = dict()
        for domain in domains:
            domains_dict[domain] = 0 
        # we want to see who rules out the least domains 
        for neighbor in neighbors:
            if neighbor in assignment:
                continue
            var_overlap, neighbor_overlap  = self.crossword.overlaps[var,neighbor]
            for neighbor_domian in self.domains[neighbor]:
                for var_domain in domains:
                    if neighbor_domian[neighbor_overlap] != var_domain[var_overlap]:
                        domains_dict[var_domain] +=1
        # we sort tje dict and then we convert it back to a list 
        sorted_domains_dict = dict(sorted(domains_dict.items(), key=lambda item: item[1]))
        domain_list = []
        for variable in sorted_domains_dict:
            domain_list.append(variable)
        return domain_list
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        ###
        # we want all variables who arent in the assignement and add the amount of domains they have 
        vars_dict =  dict()
        for varibale in self.crossword.variables:
            if varibale  in assignment:
                continue    
            vars_dict[varibale] = len(self.domains[varibale])
        mindomains = (min(vars_dict.values()))
        least_domains = []
        for value in vars_dict:
            if vars_dict[value] == mindomains:
                least_domains.append(value)
        if len(least_domains) == 1:
            return least_domains[0] 
        # now we check for most degrees 
        for degree in vars_dict:
            vars_dict[degree] = len(self.crossword.neighbors(degree))
        maxdegree = (max(vars_dict.values()))
        least_domains = []
        for value in vars_dict:
            if vars_dict[value] == maxdegree:
                least_domains.append(value)

        return least_domains[0] 
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            if self.consistent(assignment):
                return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment_copy = assignment.copy()
            assignment_copy[var] = value
            if self.consistent(assignment_copy):
                assignment[var] = value
                result = self.backtrack(assignment)
                # i got a probleam with line what is failure 
                # if result isnt failiure 
                if result != None:
                    return result
                del assignment[var]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
