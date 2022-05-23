from lib import Solver
class Main:
    def solve(path_to_inp_file: str, outfile: str =None):
        s = Solver()
        s.set_input_file(path_to_inp_file)
        if outfile is not None:
            fw = FileWriter()
            fw.set_out_file(outfile)
            s.set_writer(fw)
        s.solve()

class Examples:
    def example1():
        inp = "inputs/test_set_1/ts1_input.txt"
        out = "ts1_out.txt"
        Main.solve(inp, out)
    def example2():
        inp = "inputs/test_set_2/ts2_input.txt"
        out = "ts2_out.txt"
        Main.solve(inp, out)
    def sample():
        inp = "inputs/sample_test_set_1/sample_ts1_input.txt"
        Main.solve(inp)

# Examples.example1()
# Examples.example2()
Examples.sample()
