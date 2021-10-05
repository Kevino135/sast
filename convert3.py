#!/usr/bin/env python3

import json
import sys

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
                important_key = ['reason', 'stringsfound', 'text', 'author', 'vulnerabilityids', 'vulnerabilities']

                for all_result in data:
                        print("{}Found IssuE #{}{}".format(issue_color, index, endc))
                        for key, value in all_result.items():
                                if key.lower() in important_key:
                                        print(f"{result_key}{key.capitalize() : <30}{endc}: {custom_result_value}{value}{endc}")
                                else:
                                        print(f"{result_key}{key.capitalize() : <30}{endc}: {value}")
                        index += 1
                        print("\n")


def trufflehog(pathDir):
        print("{}>> Scanner ===> {}TruffleHog{}".format(scanner_name, scanner_name_bold, endc))
        openFile = open(f"{pathDir}/tfhog-report.json", "r")
        data = json.load(openFile)
        openFile.close()
        print_report(data)


def golangci_lint(pathDir):
        print("{}>> Scanner ===> {}Golangci-lint{}".format(scanner_name, scanner_name_bold, endc))
        openFile = open(f"{pathDir}/golangci-report.json", "r")
        try:
                data = json.load(openFile)
                data = data["Issues"]
                openFile.close()
        except:
                data = ""
        print_report(data)

def dependency_check(pathDir):
        print("{}>> Scanner ===> {}Dependency-Check{}".format(scanner_name, scanner_name_bold, endc))
        openFile = open(f"{pathDir}/dependency-check-report.json", "r")
        data = json.load(openFile)
        openFile.close()

        datas = []
        keyword = ['filename', 'filepath', 'relateddependencies', 'vulnerabilityids', 'vulnerabilities']
        for result in  data['dependencies']:
                temp = {}
                for key, value in result.items():
                        if key.lower() in keyword:
                                if key.lower() == 'relateddependencies':
                                        related = []
                                        for sub_res in result[key]:
                                                for k, v in sub_res.items():
                                                        if k.lower() == 'filepath':
                                                                related.append(v)
                                        temp[key] = related
                                elif key.lower() == 'vulnerabilities':
                                        vuln = []
                                        for sub_res in result[key]:
                                                vuln.append({'name': sub_res['name'], 'severity': sub_res['severity']})
                                        temp[key] = vuln
                                else:
                                        temp[key] = value
                datas.append(temp)
#        print(datas)
        print_report(datas)

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
        pathDir = sys.argv[1]
        headers()
        trufflehog(pathDir)
        golangci_lint(pathDir)
#        dependency_check(pathDir)

if __name__ == "__main__":
        main()
