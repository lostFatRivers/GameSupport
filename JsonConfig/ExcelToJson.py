# coding=utf-8
import xlrd
import json
import os


################################## 路径配置 ##################################

excelPath = './excel'
jsonPath = './excel'
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
    
    with open(targetPath, "w") as fp:
        if (release):
            fp.write(json.dumps(cfgDataList))
        else:
            fp.write(json.dumps(cfgDataList, indent=4))
    
    print("============= Load [" + filePath + "] Success =============")



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
    elif (valueType == "string"):
        # 字符串类型
        realResultValue = str(cellValue)
    elif (valueType.startswith("list")):
        # 数组类型
        realResultValue = []
        secondCellValueType = valueType[5:-1]
        cellValueSplit = cellValue[2:-2].split("><")
        for eachSplitValue in cellValueSplit:
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
            loadCfgToJson(os.path.join(root, f), os.path.join(jsonPath, targetJsonName), isRelease)


# loadCfgToJson('F:/Workspace/script/python/MonsterModel.xls', 'F:/Workspace/script/python/MonsterModel.json', True)

generateJsonConfig(excelPath, jsonPath, isRelease)