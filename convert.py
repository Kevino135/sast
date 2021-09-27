#!/usr/bin/env python3

import json

class bstyles:
        NO_EFFECT = "\033[0;" 
        BOLD = "\033[1;"
        UNDERLINE = "\033[2;"
        NEGATIVE1 = "\033[3;"
        NEGATIVE2 = '\033[5;'

class bcolors:
        BLACK = "30m"
        RED = "31m"
        GREEN = "32m"
        YELLOW = "33m"
        BLUE = "34m"
        PURPLE = "35m"
        CYAN = "36m"
        WHITE = "37m"
        ENDC = "0m"

index = 1
def print_report(data):
        if len(data) < 1:
                print("{}No Issue ...{}".format(issue_color, endc))
        else:
                global index
                important_key = ['reason', 'stringsfound', 'text', 'author']

                for all_result in data:
                        print("{}Issue \#{}{}".format(issue_color, index, endc))
                        for key, value in all_result.items():
                                if key.lower() in important_key:
                                        print(f"{result_key}{key.capitalize() : <30}{endc}: {custom_result_value}{value}{endc}")
                                else:
                                        print(f"{result_key}{key.capitalize() : <30}{endc}: {value}")
                        index += 1
                        print("\n")


def trufflehog():
        print("{}>> Scanner ===> {}TruffleHog{}".format(scanner_name, scanner_name_bold, endc))
        openFile = open("tfhog.json", "r")
        data = json.load(openFile)
        openFile.close()
        print_report(data)


def golangci_lint():
        print("{}>> Scanner ===> {}Golangci-lint{}".format(scanner_name, scanner_name_bold, endc))
        openFile = open("result.json", "r")
        try:
                data = json.load(openFile)
                data = data["Issues"]
                openFile.close()
        except:
                data = ""
        print_report(data)


def headers():
        print("+", "-"*46, "+", sep="")
        print("|", " "*20, "REPORT", " "*20, "|", sep="")
        print("+", "-"*46, "+", sep="")

# text color
scanner_name = bstyles.NO_EFFECT + bcolors.CYAN
scanner_name_bold = bstyles.BOLD + bcolors.CYAN
issue_color = bstyles.BOLD + bcolors.RED
result_key = bstyles.BOLD + bcolors.PURPLE
custom_result_value = bstyles.BOLD + bcolors.GREEN
endc = bstyles.NO_EFFECT + bcolors.ENDC
def main():
        headers()
        trufflehog()
        golangci_lint()

if __name__ == "__main__":
        main()
