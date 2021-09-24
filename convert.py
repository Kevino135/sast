#!/usr/bin/env python3

import json
import os

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

def headers():
	print("+", "-"*46, "+", sep="")
	print("|", " "*20, "REPORT", " "*20, "|", sep="")
	print("+", "-"*46, "+", sep="")

def main():
	scanner_name = bstyles.NO_EFFECT + bcolors.CYAN
	scanner_name_bold = bstyles.BOLD + bcolors.CYAN
	issue_color = bstyles.BOLD + bcolors.RED
	result_key_color = bstyles.BOLD + bcolors.PURPLE
	endc = bstyles.NO_EFFECT + bcolors.ENDC

#	rows, columns = os.popen('stty size', 'r').read().split()
	headers()

	print("{}>> Scanner ===> {}TruffleHog{}".format(scanner_name, scanner_name_bold, endc))

	openFile = open("tfhog.json", "r")
	data = json.load(openFile)
	openFile.close()

	index = 1

	for all_result in data:
		print("{}Issue #{}{}".format(issue_color, index, endc))
		for key, value in all_result.items():
			print("{}".format(result_key_color), f"{key.capitalize() : <13}{endc}", ": {}".format(value), sep="")
		index += 1
		print("\n")

if __name__ == "__main__":
	main()
