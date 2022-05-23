class INext:
    def get(self):
        pass
class IElement:
    pass
class IBBPath:
    def add_element(self, element: IElement):
        pass
    def get_path_id(self):
        pass
class IPathCreator:
    def create_new_paths(self, *args):
        pass
class ILoopBreaker:
    def breakable(self, *args):
        pass
class IBranchNBoundImplementation:
    def iterate(self):
        pass
class IPathIgnoreCondition:
    def ignorable(self, path: IBBPath, *args):
        pass
    def set_all_current_paths(self, paths: list[IBBPath]):
        pass
class GNext(INext):
    def set_next_get_func(self, func):
        self._func = func
    def get(self):
        return self._func(self)
class PosNext(INext):
    def get(self):
        x, y = self._pos
        mx, my = self._dim
        res = []
        if x + 1 < mx:
            res.append((x+1, y))
        if y + 1 < my:
            res.append((x,y+1))
        if x - 1 >= 0:
            res.append((x-1, y))
        if y-1>=0:
            res.append((x, y-1))
        return res
        
    def set_pos(self, pos):
        self._pos = pos
    def set_dimension(self, dim):
        self._dim = dim
class BBPath(IBBPath):
    def __init__(self):
        self._base = None
        self._elements = []
        self.set_key_func(lambda x: x._elements[0])
    def add_element(self, ele):
        self._elements.append(ele)
    def set_base_path(self, bp):
        """bp is of type BBPath"""
        self._base = bp
        self._elements = bp._elements.copy()
    def get_key(self):
        return self._key_func(self)
    def set_key_func(self, func):
        self._key_func = func
class BranchNBound(IBranchNBoundImplementation):
    def set_path_creator(self, creator: IPathCreator):
        self._path_creator = creator
    def set_breaker(self, loopBreaker: ILoopBreaker):
        self._breaker = loopBreaker
    def set_path_ignorer(self, path_igner: IPathIgnoreCondition):
        self._path_ignorer = path_igner
    def iterate(self):
        paths = self._path_creator.create_new_paths()
        paths_visited = set()
        while True:
            new_paths = []
            ignored_paths = []
            self._path_ignorer.set_all_current_paths(paths)
            for path in paths:
                if self._path_ignorer.ignorable(path, locals()):
                    ignored_paths.append(path)
                else:
                    new_paths.append(path)
                
            if self._breaker.breakable(self, locals()):
                break
            paths = new_paths.copy()
            paths += self._path_creator.create_new_paths()
            if len(new_paths) == len(paths):
                break
        return paths
class ArrayElement(IElement):
    def __init__(self, *args):
        self.value = args[0]
        self.pos = args[1]
class PathsIgnorer(IPathIgnoreCondition):
    def __init__(self):
        self.set_on_all_path_set_func(lambda x: None)
    def set_all_current_paths(self, paths):
        self._paths = paths
        self._res = self._func(paths)
    def ignorable(self, path: IBBPath, *args):
        return self._ig_func(path, self)
    def set_on_all_path_set_func(self, func):
        self._func = func
    def set_ignorable_func(self, func):
        self._ig_func = func
class PathCreator(IPathCreator):
    def __init__(self):
        self._visited = {}
    def set_array(self, mat):
        self._arr = mat
        self._pn = PosNext()
        self._pn.set_dimension((len(mat), len(mat[0])))
    def create_new_paths(self, *args):
        pos = self._next_unvisited()
        if pos is None:
            return []
        self._visited[pos] = None
        paths = self._make_path(pos)
        return [self._make_path_instance(p) for p in paths]
    def _make_path(self, pos):
        a, b = pos
        self._pn.set_pos(pos)
        positions = self._pn.get()
        new_paths = []
        for x,y in positions:
            val = self._arr[x][y]
            if val > self._arr[a][b]:
                for path in self._make_path((x,y)):
                    new_paths.append([pos]+ path)
        if len(new_paths) == 0:
            return [[pos]]
        return new_paths
    
    def _next_unvisited(self):
        for i in range(len(self._arr)):
            for j in range(len(self._arr[0])):
                if (i,j) not in self._visited:
                    return (i,j)
        
    def _make_path_instance(self, positions: list[tuple]):
        p = BBPath()
        [p.add_element(ArrayElement(self._arr[x][y], (x,y))) for x,y in positions]
        return p
class AlwaysFalse(ILoopBreaker):
    def breakable(self, *args):
        return False

class Main:
    def _filter_func(paths):
        max_0 = 0
        for p in paths:
            if len(p._elements) > max_0:
                max_0 = len(p._elements)
        return max_0
    def solve(arr):
        pc = PathCreator()
        pc.set_array(arr)

        pi = PathsIgnorer()
            
        pi.set_on_all_path_set_func(Main._filter_func)
        pi.set_ignorable_func(lambda x, pa: len(x._elements) < pa._res)

        bb = BranchNBound()
        bb.set_breaker(AlwaysFalse())
        bb.set_path_ignorer(pi)
        bb.set_path_creator(pc)

        res = bb.iterate()
        return len(res[-1]._elements)
    def example1():
        arr =  [[9, 9, 4], 
                [6, 6, 8],
                [2, 1, 1]]
        print(Main.solve(arr))