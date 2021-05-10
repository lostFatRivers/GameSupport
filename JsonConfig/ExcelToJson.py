# coding=utf-8
import xlrd
import json
import os
import shutil


################################## 路径配置 ##################################

excelPath = 'F:/workspace/Joker/github/GameSupport/JsonConfig/excel'
jsonPath = 'F:/workspace/Joker/github/ClusterServer/Ares/Support/src/main/resources/json'

javaClassPath = "F:/workspace/Joker/github/ClusterServer/Ares/Support/src/main/java/com/jokerbee/template"
javaPackage = "com.jokerbee.template"

cSharpClassPath = "F:/workspace/Joker/unity/Catan/Assets/Script/template"
cSharpJsonPath = "F:/workspace/Joker/unity/Catan/Assets/Resources/json"

isRelease = False

#############################################################################



# 读取excel表数据, 输出为json文件
def loadCfgToJson(filePath, targetPath, release):
    excelObject = xlrd.open_workbook(filePath)
    # 表数据
    mainSheet = excelObject.sheet_by_name('main')

    cfgDataList = []
    for i in range(1, mainSheet.nrows):
        cfgDataList.append(assembleRow(excelObject, mainSheet.row_values(i), 'model'))
    
    writeToJsonFile(cfgDataList, targetPath, release)
    print("============= Load [" + filePath + "] Success =============")


# 特殊数据表, 例如 GameParams
def loadSpecialCfgToJson(filePath, targetPath, release):
    excelObject = xlrd.open_workbook(filePath)
    # 表数据
    mainSheet = excelObject.sheet_by_name('main')

    cfgData = {}
    for j in range(1, mainSheet.nrows):
        fieldName = mainSheet.cell_value(j, 0)
        fieldType = mainSheet.cell_value(j, 1)
        fieldValue = mainSheet.cell_value(j, 2)
        cfgData[fieldName] = cellTrueValue(excelObject, fieldType, fieldValue)

    writeToJsonFile(cfgData, targetPath, release)
    print("============= Load [" + filePath + "] Success =============")


# 写入json文件
def writeToJsonFile(contentStr, targetPath, release):
    with open(targetPath, "w", encoding='utf-8') as fp:
        if (release):
            fp.write(json.dumps(contentStr))
        else:
            fp.write(json.dumps(contentStr, indent=4, ensure_ascii=False))


# 单行解析, 返回该行的解析对象
def assembleRow(excelObject, rowData, modelName):
    # 表数据主字段类型
    rowModel = excelObject.sheet_by_name(modelName)

    rowDataResult = {}
    for j in range(rowModel.nrows):
        # 从类型里读字段名和字段类型
        cellName = rowModel.cell_value(j, 0)
        cellValueType = rowModel.cell_value(j, 1)
        # 从行数据里读字段值
        cellValue = rowData[j]
        if cellValue is None:
            continue

        # 根据类型处理值
        rowDataResult[cellName] = cellTrueValue(excelObject, cellValueType, cellValue)
    
    return rowDataResult


# 单一字段值解析, 普通类型会被直接转换, 对象类型会递归读取表里的model进行深入解析
def cellTrueValue(excelObject, valueType, cellValue):
    realResultValue = cellValue

    if (valueType == "int"):
        # 整数类型
        realResultValue = int(cellValue)
    elif (valueType == "float"):
        # 小数类型
        realResultValue = float(cellValue)
    elif (valueType == "string"):
        # 字符串类型
        realResultValue = str(cellValue)
    elif (valueType == "list<int>" or valueType == "list<float>" or valueType == "list<string>"):
        # 基础数据数组类型
        realResultValue = []
        secondCellValueType = valueType[5:-1]
        cellValueSplit = cellValue[1:-1].split(",")
        for eachSplitValue in cellValueSplit:
            if (eachSplitValue == ""):
                continue
            realResultValue.append(cellTrueValue(excelObject, secondCellValueType, eachSplitValue))
    elif (valueType.startswith("list")):
        # 数组类型
        realResultValue = []
        secondCellValueType = valueType[5:-1]
        cellValueSplit = cellValue[2:-2].split("><")
        for eachSplitValue in cellValueSplit:
            if (eachSplitValue == ""):
                continue
            realResultValue.append(cellTrueValue(excelObject, secondCellValueType, eachSplitValue))
    else:
        # 对象类型, 类型信息在其他sheet
        cellValueSplit = cellValue.split(",")
        realResultValue = assembleRow(excelObject, cellValueSplit, valueType)
    return realResultValue


# 将目录中所有的 excel 配置表生成为 json 放到指定位置
def generateJsonConfig(excelPath, jsonPath, isRelease):
    for root, dirs, files in os.walk(excelPath):
        for f in files:
            if not f.endswith('.xls'):
                continue
            nameSplits = f.split('.')
            targetJsonName = nameSplits[0] + '.json'
            if (nameSplits[0] == "GameParams"):
                loadSpecialCfgToJson(os.path.join(root, f), os.path.join(jsonPath, targetJsonName), isRelease)
            else:
                loadCfgToJson(os.path.join(root, f), os.path.join(jsonPath, targetJsonName), isRelease)
        
        for d in dirs:
            print("dirs: " + str(d))


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

# 生成 java 文件和 c# 文件
def generateClassFile():
    replaceLine("./tools/tools.conf", "excelPath:", "    excelPath: \"" + excelPath + "\",")
    replaceLine("./tools/tools.conf", "javaClassPath:", "    javaClassPath: \"" + javaClassPath + "\",")
    replaceLine("./tools/tools.conf", "javaPackage:", "    javaPackage: \""+ javaPackage + "\"")
    replaceLine("./tools/tools.conf", "cSharpClassPath:", "    cSharpClassPath: \""+ cSharpClassPath + "\"")
    os.chdir("./tools")
    os.system("java -jar boot-1.0.1.jar")

# 拷贝一份 json 文件到 c# 工程中
def copyJsonToCSharpProject():
    try:
        shutil.rmtree(cSharpJsonPath)
    except:
        print("删除旧 res 失败.")
    shutil.copytree(jsonPath, cSharpJsonPath)




#################################### 调用 ####################################

generateJsonConfig(excelPath, jsonPath, isRelease)
generateClassFile()
copyJsonToCSharpProject()
