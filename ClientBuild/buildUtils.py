import os

# 替换文件整行函数
def replaceLine(filePath, matchText, replaceText):
    print("replaceFile: " + filePath)
    outLines = []
    readF = open(filePath, "r+", encoding='utf-8')
    for eachLine in readF.readlines():
        newLine = eachLine
        if matchText in eachLine:
            newLine = replaceText + "\n"
        outLines.append(newLine)
    readF.close()

    writeF = open(filePath,'w', encoding='utf-8')
    writeF.writelines(outLines)
    writeF.close()