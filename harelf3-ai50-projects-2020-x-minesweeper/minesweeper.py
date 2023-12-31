import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def __hash__(self):
        return hash(len(self.cells) + self.count)

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # We can only know how many of those cells are mines if their number is
        # equal to the length of the set
        if len(self.cells) == self.count:
            return set(self.cells)
        # Otherwise, we cannot tell exactly which cell is a mine and we should return empty set
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # We can only know how many of those cells are safe if we know that the count of mines in the set is zero
        if self.count == 0:
            return set(self.cells)
        # Otherwise, we cannot tell exactly which cell is a mine and we should return empty set
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            # Return 1 to update the counter of mines in MinesweeperAI
            return 1
        return 0

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if cell in self.cells:
            self.cells.remove(cell)
            # Return 0 to update the counter of safe cells in MinesweeperAI
            return 1
        return 0


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # Set of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        count = 0
        self.mines.add(cell)
        for sentence in self.knowledge:
            count += sentence.mark_mine(cell)
        return count

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        count = 0
        self.safes.add(cell)
        for sentence in self.knowledge:
            count += sentence.mark_safe(cell)
        return count

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        cells_neighbors =set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                if (i,j) in self.moves_made:
                    continue
                if i <0 or j <0:
                    continue
                if i >7 or j>7 :
                    continue
                else:
                    cells_neighbors.add((i,j))
        sentence = Sentence(cells_neighbors,count)
        self.knowledge.append(sentence)
        # adding and removing mines
        # didnt want to put it inside here couse i will use it again 
        self.self_or_mine()

        conclusions = self.infere()

        while conclusions:
            # we append all conclusions into self.knowledge 
            for sentence in conclusions:
                self.knowledge.append(sentence)

            self.self_or_mine()

            # This is a recursive function because we need to check for new conclusions after updating knowledge base
            conclusions = self.infere()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(0, self.height):
            for j in range(0, self.width):
                move = (i, j)
                if move not in self.moves_made and move not in self.mines:
                    return move

        return None

    def self_or_mine(self):
        # 
        times_to_iterate = 1
        while times_to_iterate:
            times_to_iterate = 0
            # we iterate over each sentence 
            for sentence in self.knowledge:
                # for every cell which is where we know this is safe 
                for cell in sentence.known_safes():
                    # we mark cell as safe also remove it from whole sentences 
                    self.mark_safe(cell)
                    times_to_iterate += 1
                for cell in sentence.known_mines():
                    self.mark_mine(cell)
                    times_to_iterate += 1

            for cell in self.safes:
                times_to_iterate += self.mark_safe(cell)
            for cell in self.mines:
                times_to_iterate += self.mark_mine(cell)

    def infere(self):

        conclusions = []
        empty = []

        for sentence_1 in self.knowledge:
            if sentence_1.cells == set():
                empty.append(sentence_1)
                continue
            for sentence_2 in self.knowledge:
                if sentence_2.cells == set():
                    empty.append(sentence_2)
                    continue
                if sentence_1 != sentence_2:
                    # we see if sentence inside and not the same add new sentence
                    if sentence_2.cells.issubset(sentence_1.cells):
                        new_set = sentence_1.cells.difference(sentence_2.cells)
                        new_count = sentence_1.count - sentence_2.count
                        new_sentence = Sentence(new_set, new_count)

                        # Check is new sentence is already in knowledge base
                        if new_sentence not in self.knowledge:
                            conclusions.append(new_sentence)

        self.knowledge = [i for i in self.knowledge if i not in empty]

        return conclusions
