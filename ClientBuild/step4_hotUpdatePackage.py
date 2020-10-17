import os
import sys
import shutil
import platform

from buildUtils import replaceLine

def hotUpdatePackageGenerate(platformRootPath, apkTargetPath, cocosPath, version, cdnType, device, packageVersion):
    # 改 main.js
    replaceLine(platformRootPath + "/main.js", "window._game_res_version =", "	window._game_res_version = '" + packageVersion + "';")

    if device != "localTest":
        hotTargetPath = apkTargetPath + "/hotUpdate"
        if(os.path.exists(hotTargetPath + "/project.manifest")):
            os.remove(hotTargetPath + "/project.manifest")

        if(os.path.exists(hotTargetPath + "/version.manifest")):
            os.remove(hotTargetPath + "/version.manifest")

        try:
            shutil.rmtree(hotTargetPath + "/res")
        except:
            print("删除旧 res 失败.")

        try:
            shutil.rmtree(hotTargetPath + "/src")
        except:
            print("删除旧 src 失败.")

        shutil.copy(cocosPath + "/assets/project.manifest", hotTargetPath)
        shutil.copy(cocosPath + "/assets/version.manifest", hotTargetPath)
        shutil.copytree(platformRootPath + "/res", hotTargetPath + "/res")
        shutil.copytree(platformRootPath + "/src", hotTargetPath + "/src")

        os.chdir(hotTargetPath)

        hotZipName="plane_{0}_{1}_{2}.zip".format(version, cdnType, packageVersion)

        if(os.path.exists(hotZipName)):
            os.remove(hotZipName)

        if ("Windows" in platform.system()):
            os.system("F:/Program/WinRAR/WinRAR.exe a -r " + hotZipName + " ./project.manifest ./version.manifest ./res ./src")
        else:
            os.system("zip -r " + hotZipName + " ./project.manifest ./version.manifest ./res ./src")
