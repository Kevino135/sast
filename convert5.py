#!/usr/bin/env python3

import json
import sys
import re
from fpdf import FPDF
from datetime import datetime

title = 'REPORT'
idx_issue = 1

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 0, 0)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, label):
        # Arial 12
        self.set_font('Helvetica', 'B', 10)
        # Background color
        self.set_fill_color(0,139,139)
        self.set_text_color(255, 255, 255)
        # Title
        self.cell(0, 6, '[+] Scanner ===> %s' % (label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, data):
        if len(data) < 1:
            self.set_text_color(178, 34, 34)
            self.cell(0, 0, "No Issue ...")
        else:
            global idx_issue
            important_key = ['reason', 'stringsfound', 'text', 'author', 'vulnerabilityids', 'vulnerabilities', 'offender', 'rule']

            self.set_font('Helvetica', '', 8)
            for result in data:
                self.set_text_color(178,34,34)
                self.cell(0, 0, "Found Issue #" + str(idx_issue))
                self.ln(4)
                for key, value in result.items():
                    if len(str(value)) > 100:
                        heights = 4.5
                    else:
                        heights = 2
                    
                    if key.lower() in important_key:
                        self.set_text_color(70,130,180)
                        self.cell(40, heights, 
                              txt = (str(key)).capitalize(), 
                              border = 0, 
                              ln = 0, 
                              align = '', 
                              fill = False, 
                              link = '')
                        self.set_text_color(34,139,34)
                        self.multi_cell(0, heights, ": " + (str(value)).translate(str.maketrans({"\n": r"\\n"})))
                        self.ln()
                    else:
                        self.set_text_color(70,130,180)
                        self.cell(40, heights, 
                              txt = (str(key)).capitalize(), 
                              border = 0, 
                              ln = 0, 
                              align = '', 
                              fill = False, 
                              link = '')
                        self.set_text_color(0, 0, 0)
                        self.multi_cell(0, heights, ": " + (str(value)).translate(str.maketrans({"\n": r"\\n"})))
                        self.ln()
                idx_issue += 1
                self.ln(9)

    def print_chapter(self, title, data):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(data)

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
                important_key = ['reason', 'stringsfound', 'text', 'author', 'vulnerabilityids', 'vulnerabilities', 'offender', 'rule']

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
        
        pdf.print_chapter("TruffleHog", data)


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

        pdf.print_chapter("Golangci-lint", data)

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

def gitleaks(pathDir):
        print("{}>> Scanner ===> {}Gitleaks{}".format(scanner_name, scanner_name_bold, endc))
        openFile = open(f"{pathDir}/gitleaks-report.json", "r")
        content = openFile.readlines()
        openFile.close()

        data = []
        keyword = ['line', 'linenumber', 'offender', 'rule', 'file', 'tags']
        for i in content:
                datas = json.loads(i)
                dat = json.dumps(datas, sort_keys=True)
                datas = json.loads(dat)
                temp = {}
                for key, value in datas.items():
                        if key.lower() in keyword:
                                temp[key] = value
                data.append(temp)
#        print(data)
        print_report(data)

        pdf.print_chapter("Gitleaks", data)

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

# PDF init
pdf = PDF()
pdf.set_title(title)

def main():
        pathDir = sys.argv[1]
        headers()
        trufflehog(pathDir)
        golangci_lint(pathDir)
#        dependency_check(pathDir)
        gitleaks(pathDir)

        now = str(datetime.now()).split('.')
        fileName = str(now[0].replace(':', '_'))

        pdf.output(f'{fileName}.pdf', 'F')

if __name__ == "__main__":
        main()
