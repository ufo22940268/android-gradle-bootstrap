#! ../env/bin/python
# -*- coding: utf-8 -*-
from gradlebs import create_app
from gradlebs.models import db
from gradlebs import packages
import subprocess

import os.path
from os.path import join

BS_PATH = '/tmp/gradle-sample'

class TestPackage:

    @classmethod
    def setup_class(cls):
        subprocess.check_call(["rm", "-r", BS_PATH])
    
    def test_packages(self):
        packages.copy()
        
        assert os.path.exists(BS_PATH)

        package_path = "com.hongbosb"
        packages.customize(package_path);
        am = open(join(BS_PATH, "src/main/AndroidManifest.xml"))
        assert am.read().find(package_path) != -1

        new_path = join(BS_PATH, 'src/main/java/', "/".join(package_path.split('.')))
        assert os.path.exists(new_path)

        #Check java import path.
        main_act = open(join(BS_PATH, 'src/main/java/', "/".join(package_path.split('.')),
                             'MainActivity.java'))
        assert main_act.read().find('package ' + package_path) != -1
