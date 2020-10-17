import os

from buildUtils import replaceLine


def androidGradleBuild(androidPath, packageVersion):
    os.chdir(androidPath)
    os.system("svn up")

    replaceLine(androidPath + "/app/build.gradle", "versionCode", "        versionCode " + packageVersion[4])
    replaceLine(androidPath + "/app/build.gradle", "versionName", "        versionName '" + packageVersion + "'")
    
    # 开始构建android包
    os.system("gradlew clean")
    # os.system("gradlew assembleRelease")