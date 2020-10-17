import os

from buildUtils import replaceLine

def jsonGenerate(toolsPath, cocosPath, documentPath):
    # 修改生成表工具配置
    toolConfigFile = toolsPath + "/config/tools.conf"
    replaceLine(toolConfigFile, "configPath", "configPath = " + documentPath)
    replaceLine(toolConfigFile, "clientPath", "clientPath = " + cocosPath + "/assets")

    # 更新表
    os.chdir(documentPath)
    os.system("svn up")

    # 生成表
    os.chdir(toolsPath)
    os.system("java -classpath tools.jar com.joker.tools.Excel2code")

    os.chdir(cocosPath + "/assets")
    os.system("svn up")