import os
import shutil
import zipfile
from zipfile import ZipFile

from src import ZIPSTORED


def unzip_apk(zip_name):
    with ZipFile(zip_name, 'r') as zipObject:
        fileNameList = zipObject.namelist()
        zipObject.extractall('release')
        for fileName in fileNameList:
            print(fileName)
        zipObject.close()


def zip_new_apk():
    zipFile = zipfile.ZipFile('release.RE.zip', 'w', zipfile.ZIP_DEFLATED)
    zip_apk_dir('release/', zipFile)
    zipFile.close()
    shutil.move("release.RE.zip", "release.RE.apk")
    shutil.rmtree('release')


def sign_apk():
    # java -jar uber-apk-signer.jar --allowResign -a release.RE.apk
    val = os.system('java -jar uber-apk-signer.jar --allowResign -a release.RE.apk')
    print(val)


def zip_apk_dir(path, zipFile):
    for root, dirs, files in os.walk(path):
        for file in files:
            if type(file) is str:
                if file.endswith('.so') and ZIPSTORED or file.endswith('resources.arsc'):
                    zipFile.write(os.path.join(root, file),
                                  os.path.relpath(os.path.join(root.replace('release/', ''), file),
                                                  os.path.join(path, '..')), zipfile.ZIP_STORED)
                else:
                    zipFile.write(os.path.join(root, file),
                                  os.path.relpath(os.path.join(root.replace('release/', ''), file),
                                                  os.path.join(path, '..')), zipfile.ZIP_DEFLATED)
            else:
                zipFile.write(os.path.join(root, file),
                              os.path.relpath(os.path.join(root.replace('release/', ''), file),
                                              os.path.join(path, '..')),
                              zipfile.ZIP_DEFLATED)


def replace_apk_file(file_path, item_path):
    # 移动文件 重复会覆盖
    # 目标是文件夹 直接进去
    shutil.move(file_path, item_path)


if __name__ == '__main__':
    unzip_apk('demo.apk')
    zip_new_apk()
    sign_apk()
