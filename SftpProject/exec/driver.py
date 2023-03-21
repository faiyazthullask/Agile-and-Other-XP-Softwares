from connections import *

"""
This is the program where the execution starts.
"""
if __name__ == "__main__":
    try:
        ask()
    except Exception as e:
        print(f"Error occured:{e}. Please Try Again")
        exit()