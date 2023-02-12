#!usr/bin/python

# -*- coding: utf-8 -*-

__author__ = 'LinFan'

class LcovInfo:
    def __init__(self, infoFilePath):
        self.infoFilePath = infoFilePath
        self.fileCovs = []
        #解析info文件
        try:
            with open(self.infoFilePath, "r") as file:
                lines = file.readlines()
                singeFile = []
                for line in lines:
                    singeFile.append(line)
                    if line.startswith("end_of_record"):
                        fileCov = LcovFileCov(singeFile)
                        self.fileCovs.append(fileCov)
                        singeFile = []
        except FileNotFoundError:
            return

class LcovFileCov:
    def __init__(self, lines):
        self.TN = ""
        self.SF = ""
        self.FNs = []
        self.FNDAs = []
        self.BRDAs = []
        self.DAs = []
        for line in lines:
            lineSpilt = line.split(":")
            #TN:<test name>
            if line.startswith("TN:"):
                self.TN = line
            #SF:<absolute path to the source file>
            if line.startswith("SF:"):
                self.SF = line.replace('SF:','').replace('\n','')
                # print(self.SF)
            #FN:<execution count>,<function name>
            if line.startswith("FN:"):
                stripLine = line.replace('FN:','').replace('\n','')
                contentSplit = stripLine.split(",")
                FN = LcovFN(contentSplit[0], contentSplit[1])
                self.FNs.append(FN)
                # print(FN.lineNum)
                # print(FN.functionName)
            #FNDA:<execution count>,<function name>
            if line.startswith("FNDA:"):
                stripLine = line.replace('FNDA:','').replace('\n','')
                contentSplit = stripLine.split(",")
                FNDA = LcovFNDA(contentSplit[0], contentSplit[1])
                self.FNDAs.append(FNDA)
                # print(FNDA.count)
                # print(FNDA.functionName)
            #FNF:<number of functions found>
            if line.startswith("FNF:"):
                self.FNF = int(lineSpilt[1])
                # print(self.FNF)
            #FNH:<number of function hit>
            if line.startswith("FNH:"):
                self.FNH = int(lineSpilt[1])
                # print(self.FNH)
            #DA:<line number>,<execution count>[,<checksum>]
            if line.startswith("DA:"):
                contentSplit = lineSpilt[1].split(",")
                DA = LcovDA(contentSplit[0],contentSplit[1])
                self.DAs.append(DA)
                # print(DA.lineNum)
                # print(DA.count)
            #BRDA:<line number>,<block number>,<branch number>,<taken>
            if line.startswith("BRDA:"):
                stripLine = line.replace('BRDA:','').replace('\n','')
                contentSplit = stripLine.split(",")
                BRDA = LcovBRDA(contentSplit[0],contentSplit[1],contentSplit[2],contentSplit[3])
                self.BRDAs.append(BRDA)
                # print(BRDA.lineNum)
                # print(BRDA.blockNum)
                # print(BRDA.branchNum)
                # print(BRDA.taken)
            #BRF:<number of branches found>
            if line.startswith("BRF:"):
                self.BRF = int(lineSpilt[1])
                # print(self.BRF)
            #BRH:<number of branches hit>
            if line.startswith("BFH:"): #lcov 工具的bug，已修复，改为BRH，但需要做兼容
                self.BFH = int(lineSpilt[1])
                self.BRH = int(lineSpilt[1])
                # print(self.BRH)
            if line.startswith("BRH:"):
                self.BFH = int(lineSpilt[1])
                self.BRH = int(lineSpilt[1])
                # print(self.BRH)
            #LF:<number of instrumented lines>
            if line.startswith("LF:"):
                self.LF = int(lineSpilt[1])
                # print(self.LF)
            #LH:<number of lines with a non-zero execution count>
            if line.startswith("LH:"):
                self.LH = int(lineSpilt[1])
                # print(self.LH)

class LcovFN:
    def __init__(self, lineNum, functionName):
        self.lineNum = int(lineNum)
        self.functionName = functionName

class LcovFNDA:
    def __init__(self, count, functionName):
        self.count = int(count)
        self.functionName = functionName

class LcovBRDA:
    def __init__(self, lineNum, blockNum, branchNum, taken):
        self.lineNum = int(lineNum)
        self.blockNum = int(blockNum)
        self.branchNum = int(branchNum)
        self.taken = taken

class LcovDA:
    def __init__(self, lineNum, count):
        self.lineNum = int(lineNum)
        self.count = int(count)