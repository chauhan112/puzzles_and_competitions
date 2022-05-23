import os
class Case:
    def __init__(self, content):
        self.set_content(content)
    def get(self):
        return self._content
    def set_content(self, content):
        self._content = content
    def set_line(self, line: str):
        self.set_content([int(c) for c in line])

class IReader:
    def get(self) :
        pass
class CmdReader(IReader):
    def get(self):
        nr_cases = int(input().strip())
        cases = []
        for i in range(nr_cases):
            inp = input().strip()
            cases.append(Case([int(c) for c in inp]))
        return cases
class Reader:
    def set_string(self, content: str):
        self._content = content.strip()
    def get(self):
        lines = self._content.splitlines()
        lines = lines[1:]
        return [Case([int(c) for c in line]) for line in lines]
    def set_file(self, file):
        self._inp_file = file
        with open(self._inp_file, "r", encoding="utf-8") as f:
            self.set_string(f.read())
class SingleCaseSolver:
    def set_case(self, case: Case):
        self._case = case
    def solve(self):
        arr = self._case.get()
        min_ind = self.indices_sort(arr)
        t = len(arr)
        if t > 2:
            return arr[min_ind[0]]
        if t == 2:
            return arr[1]
        return arr[0]
    def indices_sort(self, arr):
        return list(map(lambda x: x[0], sorted(enumerate(arr), key= lambda x: x[1])))
    
class IWriter:
    def write(self, val):
        pass
class Write2Cmd(IWriter):
    def write(self, val):
        print(val)
class Write2File(IWriter):
    def __init__(self):
        self.set_file("output.txt")
    def write(self, val):
        with open(self._output, "a", encoding="utf-8") as f:
            f.write(str(val) + "\n")
    def set_file(self, file: str):
        self._output = file
        if os.path.exists(self._output):
            os.remove(self._output)
class Solver:
    def set_reader(self, reader: IReader):
        self._reader = reader
    def get_results(self):
        cases = self._reader.get()
        for case in cases:
            self._scs.set_case(case)
            self._writer.write(self._scs.solve())
    def set_writer(self, writer: IWriter):
        self._writer = writer
    def set_single_case_solver(self, sole):
        self._scs = sole
        
class Main:
    def solve(content: str = None,inp_file: str =None):
        r = Reader()
        if content is None:
            r.set_file(inp_file)
        else:
            r.set_string(content)
        w = Write2Cmd()
        s = Solver()
        s.set_single_case_solver(SingleCaseSolver())
        s.set_reader(r)
        s.set_writer(w)
        s.get_results()
    def example1():
        inp = """3
12
132
487456398
        """
        Main.solve(inp)

Main.example1()