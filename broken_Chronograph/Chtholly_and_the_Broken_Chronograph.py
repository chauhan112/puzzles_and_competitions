class IOps:
    def execute(self):
        pass
class InputCase:
    def __init__(self, arr):
        self._arr = arr
    def set_state(self, arr):
        self._activated_arr = arr
    def apply(self, ops):
        ops.set_model(self)
        ops.execute()
class INext:
    def get(self):
        pass
class Challenge:
    def parse_list(func, line):
        return [func(v) for v in line.strip().split()]
    def parse_int_list(line):
        return Challenge.parse_list(int, line)
    
class ContentNext(INext):
    def __init__(self):
        self._index = 0
    def get(self):
        line = self._lines[self._index]
        self._index += 1
        return line
    def set_content(self, content: str):
        self._lines = content.strip().splitlines()
class CMDInput(INext):
    def get(self):
        return input().strip()
class DataSet:
    def set_data(self, data):
        self._data = data
    def set_model(self, model: InputCase):
        self._model = model
        
class Block(IOps, DataSet):
    def execute(self):
        idx = self._data[0] -1
        self._model._activated_arr[idx] = 0
class Activate(IOps, DataSet):
    def execute(self):
        idx = self._data[0] -1
        self._model._activated_arr[idx] = 1
class Add(IOps, DataSet):
    def execute(self):
        l, r,v = self._data
        for i in range(l-1, r):
            if self._model._activated_arr[i] == 1:
                self._model._arr[i] += v
class Print(IOps, DataSet):
    def execute(self):
        l, r = self._data
        t = sum(self._model._arr[l-1:r])
        print(t)
    
ops_map ={
    1: Block,
    2: Activate,
    3: Add,
    4: Print
}
class LineByLineReader:
    def set_content(self, content: str):
        self._content = content
        nter = ContentNext()
        nter.set_content(content)
        self.set_nexter(nter)
    def set_nexter(self, nexter: INext):
        self._nexter = nexter
        self._inp_case = None
        self._ops = None
    def get(self):
        if self._inp_case is None:
            self._parse()
        return self._inp_case
    def get_ops(self):
        if self._ops is None:
            self._parse()
        return self._ops
    def _parse(self):
        n, q = Challenge.parse_int_list(self._nexter.get())
        arr = Challenge.parse_int_list(self._nexter.get())
        blocked_info = Challenge.parse_int_list(self._nexter.get())
        ops =[]
        for i in range(q):
            ops_val = Challenge.parse_int_list(self._nexter.get())
            ops_type = ops_val[0]
            op = ops_map[ops_type]()
            op.set_data(ops_val[1:])
            ops.append(op)
        self._inp_case = InputCase(arr)
        self._inp_case.set_state(blocked_info)
        self._ops = ops

class Main:
    def solve(content):
        lblr = LineByLineReader()
        lblr.set_content(content)

        ic = lblr.get()
        for op in lblr.get_ops():
            ic.apply(op)
    def example1():
        ct = """4 8
            4 2 5 3
            1 0 0 1
            2 3
            3 1 4 1
            1 3
            4 1 4
            1 1
            2 2
            3 1 3 2
            4 1 4"""
        Main.solve(ct)
Main.example1()