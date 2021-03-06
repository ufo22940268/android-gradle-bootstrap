import zipfile
import subprocess
from bs4 import BeautifulSoup
from os.path import join
import os
import uuid

BS_PATH = '/tmp/gradle-sample'

def copy():
    subprocess.check_call(["cp", "-rf", "gradle-sample", "/tmp"])

def customize(package_name = "com.test", app_name = 'example'):
    #init
    subprocess.call(["rm", "-r", BS_PATH])
    
    #copy sample project to tmp
    copy()

    #customize
    with open(join(BS_PATH, "src/main/AndroidManifest.xml"), "r") as am:
        soup = BeautifulSoup(am);
        soup.find("manifest")['package'] = package_name
        customized_str = soup.prettify()

    with open(join(BS_PATH, "src/main/AndroidManifest.xml"), "w") as am:
        am.write(customized_str)

    # rename package path
    sample_path = "de/goddchen/android/gradle/helloworld"
    ori_path = BS_PATH + '/src/main/java/' + sample_path
    new_path = BS_PATH + '/src/main/java/' + "/".join(package_name.split('.'))
    os.renames(ori_path, new_path)

    #rename package path of all java files.
    with open(join(BS_PATH, 'src/main/java', '/'.join(package_name.split('.')), 'MainActivity.java'), 'r') as main_act:
        act_str = main_act.read()
        act_str = act_str.replace('package ' + '.'.join(sample_path.split('/')),
                        'package ' + '.'.join(package_name.split('/')))
        main_act.close()
        
    with open(join(BS_PATH, 'src/main/java', '/'.join(package_name.split('.')), 'MainActivity.java'), 'w') as main_act:    
        main_act.write(act_str)
        main_act.close()

    #Replace app name
    with open(join(BS_PATH, 'src/main/res/values/strings.xml'), 'r') as strings_file:
        soup = BeautifulSoup(strings_file)
        soup.find_all('string')[0].string = app_name
        strings_str = soup.prettify()

    with open(join(BS_PATH, 'src/main/res/values/strings.xml'), 'w') as strings_file:    
        strings_file.write(strings_str)
        
    #zip file
    zip_file_name = str(uuid.uuid4()) + ".zip"
    f = zipfile.ZipFile(join('gradlebs/static/public/zipfiles', zip_file_name),'w',zipfile.ZIP_DEFLATED) 

    for dirpath, dirnames, filenames in os.walk(BS_PATH): 
        for filename in filenames:
            final_name = os.path.join(dirpath,filename)
            f.write(final_name, final_name.replace('tmp', '')) 
    f.close()
    return zip_file_name
