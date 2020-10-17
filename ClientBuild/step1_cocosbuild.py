import os
import time
import sys
import platform
import shutil
import zipfile

from buildUtils import replaceLine
from step2_documentBuild import jsonGenerate
from step3_cocoscreator import cocoscreatorBuild
from step4_hotUpdatePackage import hotUpdatePackageGenerate
from step5_androidBuild import androidGradleBuild

cocosPath = "D:/WorkSpace/client/game_trunk"
buildPath = "D:/cocos/game"
documentPath = "D:/WorkSpace/document/game/trunk"
toolsPath = "D:/WorkSpace/documentTools/tools"

ksPath = "E:/cer/android/game.keystore"
ksPassword = "1234321"
ksAlias = "Game"
ksAliasPassword = "1234321"

platformRootPath = buildPath + "/jsb-link"
androidPath = platformRootPath + "/frameworks/runtime-src/proj.android-studio"
iosPath = platformRootPath + "/frameworks/runtime-src/proj.ios_mac"
apkTargetPath = "D:/cocos/space/package"

cocosCreatorPath = "F:/Program/CocosDashboard/resources/.editors/Creator/2.3.3/CocosCreator.exe"

# cocoscreator build 是否开启调试
isDebug = "false"

appName = "Game"

# gameType 游戏id
gameType = "10021102"

timeStemp = time.strftime("%Y%m%d", time.localtime())
dayStemp = time.strftime("%m%d", time.localtime())

# packageId 打包id
packageId = gameType + timeStemp

channel = "xiaomi" + dayStemp

# main.js 修改
packageVersion = "1.0.4"

# 设备和渠道类型, localTest 表示打内部测试包, 不热更.
device = "android"

# 包名
bundleId = "com.joker.game"

# cdn类型: online/test
cdnType = "online"

# 热更版本 & 热更地址
version = "1.0.4.1"
hotUrl = ""

# 1:生成表, 2:生表+构建, 3:生表+构建+热更包, 4:生表+构建+热更包+打apk
executeType = "1"

argumentLength = len(sys.argv)

if argumentLength > 1:
    packageVersion = sys.argv[1]
    version = sys.argv[2]
    cdnType = sys.argv[3]
    executeType = sys.argv[4]

configFilePath = "{0}/packConfig/{1}/{2}/GameConfig.js".format(cocosPath, device, cdnType)


if device == "android":
    if cdnType == "online":
        hotUrl = "http://game.joker.com/hotupdate/online/v0.0.0"
    elif cdnType == "test":
        hotUrl = "http://game.joker.com/hotupdate/test/v0.0.0"

elif device == "ios":
    if cdnType == "online":
        hotUrl = "http://ios/online/v0.0.0"
    elif cdnType == "test":
        hotUrl = "http://ios/test/v0.0.0"

else:
    hotUrl = ""

if hotUrl == "":
    print("no valid hotUrl, change device to 'localTest'")
    device = "localTest"
    configFilePath = cocosPath + "/packConfig/localTest/GameConfig.js"

print("=============== cocoscreator build isDebug: " + isDebug)
print("=============== packageId: " + packageId)
print("=============== device: " + device)
print("=============== cdnType: " + cdnType)
print("=============== manifest version: " + version)
print("=============== hotUrl: " + hotUrl)
print("=============== config file path: " + configFilePath)
print("=============== channel: " + channel)

# 代码更新
os.chdir(cocosPath + "/assets")
os.system("svn up")

############## 生表 ##############
jsonGenerate(toolsPath, cocosPath, documentPath)
if executeType == "1":
    sys.exit(0)

############## 构建 ##############
cocoscreatorBuild(configFilePath, cocosPath, cocosCreatorPath, packageId, version, channel, device, isDebug, buildPath, bundleId, ksPath, ksPassword, ksAlias, ksAliasPassword, hotUrl, platformRootPath)
if executeType == "2":
    sys.exit(0)

############## 热更包 ##############
hotUpdatePackageGenerate(platformRootPath, apkTargetPath, cocosPath, version, cdnType, device, packageVersion)
if executeType == "3":
    sys.exit(0)

############## 安卓 apk ##############
androidGradleBuild(androidPath, packageVersion)