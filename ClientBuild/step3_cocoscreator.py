import os
import sys
import shutil

from buildUtils import replaceLine

def cocoscreatorBuild(configFilePath, cocosPath, cocosCreatorPath, packageId, version, channel, device, isDebug, buildPath, bundleId, ksPath, ksPassword, ksAlias, ksAliasPassword, hotUrl, platformRootPath):
    # 替换配置文件
    shutil.copy(configFilePath, cocosPath + "/assets/scripts/Game/config/")

    gameConfigFile = cocosPath + "/assets/scripts/Game/config/GameConfig.js"
    # 改 packageId
    replaceLine(gameConfigFile, "packageId", "    packageId: '" + packageId + "',")

    # 改 显示的版本号
    replaceLine(gameConfigFile, "version", "    version: '" + version + "',")

    # 改 渠道
    replaceLine(gameConfigFile, "channel", "    channel: '" + channel + "',")

    buildCommondStr = "{0} --path {1} --build 'platform=android;debug={2};buildPath={3};packageName={4};useDebugKeystore=false;keystorePath={5};keystorePassword={6};keystoreAlias={7};keystoreAliasPassword={8}'".format(cocosCreatorPath, cocosPath, isDebug, buildPath, bundleId, ksPath, ksPassword, ksAlias, ksAliasPassword)

    versionCommondStr = "node version_generator.js -v {0} -u {1} -s {2}".format(version, hotUrl, platformRootPath)

    # 第一遍构建和生成 manifest 文件
    if device != "localTest":
        os.system(buildCommondStr)
        os.chdir(cocosPath)
        os.system(versionCommondStr)

    # 第二遍构建
    os.system(buildCommondStr)

    # 第二遍生成 manifest 文件
    if device != "localTest":
        os.chdir(cocosPath)
        os.system(versionCommondStr)

    os.system("svn revert " + gameConfigFile)