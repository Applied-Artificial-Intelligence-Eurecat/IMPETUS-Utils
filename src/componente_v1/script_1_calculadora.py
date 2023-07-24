import sys

def main():
    arg_list = sys.argv
    operand_1 = int(arg_list[1])
    operand_2 = int(arg_list[2])
    result = operand_1 * operand_2
    print(result)
    return 0

if __name__ == "__main__":
    main()
