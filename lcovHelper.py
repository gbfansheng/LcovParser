#!usr/bin/python

# -*- coding: utf-8 -*-

__author__ = 'LinFan'

import lcovInfoClass

#写入文件
def writeLcovInfo(lcovInfo):
    print(lcovInfo.infoFilePath)
    print(len(lcovInfo.fileCovs))
    with open(lcovInfo.infoFilePath, "w") as file:
        for fileCov in lcovInfo.fileCovs:
            SFLine = "SF:" + fileCov.SF + "\n"
            file.write(SFLine)
            file.write(SFLine)
            for FN in fileCov.FNs:
                FNLine = "FN:" + str(FN.lineNum) + "," + FN.functionName + "\n"
                file.write(FNLine)
            for FNDA in fileCov.FNDAs:
                FNDALine = "FNDA:" + str(FNDA.count) + "," + FNDA.functionName + "\n"
                file.write(FNDALine)
            FNFLine = "FNF:" + str(fileCov.FNF) + "\n"
            file.write(FNFLine)
            FNHLine = "FNH:" + str(fileCov.FNH) + "\n"
            file.write(FNHLine)
            for DA in fileCov.DAs:
                DALine = "DA:" + str(DA.lineNum) + "," + str(DA.count) + "\n"
                file.write(DALine)
            for BRDA in fileCov.BRDAs:
                BRDALine = "BRDA:" + str(BRDA.lineNum) + "," + str(BRDA.blockNum) + "," + str(BRDA.branchNum) + "," + BRDA.taken + "\n"
                file.write(BRDALine)
            BRFLine = "BRF:" + str(fileCov.BRF) + "\n"
            file.write(BRFLine)
            BRHLine = "BRH:" + str(fileCov.BRH) + "\n"
            file.write(BRHLine)
            LFLine = "LF:" + str(fileCov.LF) + "\n"
            file.write(LFLine)
            LHLine = "LH:" + str(fileCov.LH) + "\n"
            file.write(LHLine)
            file.write("end_of_record\n")

#合并info文件
def mergeLcovInfo(fileInfoList, resultInfoPath):
    # print("start merge")
    # print(fileInfoList)
    resultLcovInfo = lcovInfoClass.LcovInfo(resultInfoPath)
    resultLcovInfo.fileCovs = []
    if len(fileInfoList) > 0:
        firstFileInfo = fileInfoList[0]
        for fileCov in firstFileInfo.fileCovs:
            targetSF = fileCov.SF
            print(targetSF)
            targetCovs = findSingleFileCovs(targetSF, fileInfoList)
            mergedCov = mergeSingeFlieCovs(targetCovs)
            resultLcovInfo.fileCovs.append(mergedCov)
    return resultLcovInfo

#找出相同文件的覆盖报告
def findSingleFileCovs(SF, fileInfoList):
    covList = []
    for fileInfo in fileInfoList:
        for fileCov in fileInfo.fileCovs:
            if fileCov.SF == SF:
                covList.append(fileCov)
    return covList

#合并单个文件的覆盖数据
def mergeSingeFlieCovs(covsList):
    resultFileCov = lcovInfoClass.LcovFileCov([])
    resultFileCov.TN = covsList[0].TN
    resultFileCov.SF = covsList[0].SF
    resultFileCov.FNs = covsList[0].FNs
    resultFileCov.FNDAs = mergeFNDA(covsList)
    resultFileCov.FNF = covsList[0].FNF
    resultFileCov.FNH = caculateFNH(resultFileCov.FNDAs)
    resultFileCov.DAs = mergeDA(covsList)
    resultFileCov.BRDAs = mergeBRDA(covsList)
    resultFileCov.BRF = covsList[0].BRF
    resultFileCov.BRH = caculateBRH(resultFileCov.BRDAs)
    resultFileCov.LF = covsList[0].LF
    resultFileCov.LH = covsList[0].LH #TODO 看一下LH如何计算
    return resultFileCov

#累计FNDA
def mergeFNDA(covsList):
    resultFNDAs = []
    for fileCov in covsList:
        for FNDA in fileCov.FNDAs:
            containFNDA = False
            for i in range(len(resultFNDAs)):
                rFNDA = resultFNDAs[i]
                if rFNDA.functionName == FNDA.functionName:
                    rFNDA.count = rFNDA.count + FNDA.count
                    containFNDA = True
            if containFNDA == False:
                resultFNDAs.append(FNDA)
    # for fnda in resultFNDAs:
    #     print(str(fnda.count) + fnda.functionName)
    return resultFNDAs

#累计FNH
def caculateFNH(FNDAs):
    #计算FNH
    FNH = 0
    for FNDA in FNDAs:
        if FNDA.count != 0:
            FNH = FNH + 1
    return FNH

#累计DA
def mergeDA(covsList):
    resultDAs = []
    for fileCov in covsList:
        #累计DA
        for DA in fileCov.DAs:
            containDA = False
            for i in range(len(resultDAs)):
                rDA = resultDAs[i]
                #若存在，则相加
                if rDA.lineNum == DA.lineNum:
                    rDA.count = rDA.count + DA.count
                    containDA = True
            #若不存，则加入队列
            if containDA == False:
                resultDAs.append(DA)
        resultDAs.sort(key=lambda DA: DA.lineNum)
    return resultDAs
    
#累计BRDA
def mergeBRDA(covsList):
    resultBRDAs = []
    for fileCov in covsList:
        #累计BRDA
        for BRDA in fileCov.BRDAs:
            containBRDA = False
            for i in range(len(resultBRDAs)):
                rBRDA = resultBRDAs[i]
                if rBRDA.lineNum == BRDA.lineNum and rBRDA.blockNum == BRDA.blockNum and rBRDA.branchNum == BRDA.branchNum:  
                    #若存在，则相加
                    containBRDA = True
                    rTaken = 0
                    if rBRDA.taken == "-":
                        rTaken = 0
                    else:
                        rTaken = int(rBRDA.taken)
                    if BRDA.taken == "-":
                        taken = 0
                    else:
                        taken = int(BRDA.taken)
                    rTaken = rTaken + taken
                    if rTaken == 0:
                        rBRDA.taken = "-"
                    else:
                        rBRDA.taken = str(rTaken)
            #若不存，则加入队列
            if containBRDA == False:
                resultBRDAs.append(BRDA)
    return resultBRDAs

#累计BRH
def caculateBRH(BRDAs):
    #计算BRH
    BRH = 0
    for BRDA in BRDAs:
        # print(""+ str(BRDA.lineNum) + "," + str(BRDA.blockNum) + "," + str(BRDA.branchNum) +"," + BRDA.taken)
        if BRDA.taken != "-" and BRDA.taken != "0":
            BRH = BRH + 1
    return BRH