import os
import re
import sys
import zipfile
from shutil import move, copyfile, copy
import argparse
import autograder

class grading:
    def __init__(self,settings):
        self.AssignmentName = settings['assignmentName']
        self.FromFiles = settings['ImportFiles']
        # if the file is under solution folder
        self.IsInSolutionFolder = bool(settings['IsInSolutionFolder'])
        self.assignmentPath = settings['assignmentPath']
        self.subdirName = settings['subdirName']

        self.ToFiles = list(self.FromFiles)
        if self.IsInSolutionFolder:
            self.FromFiles = ['solution/' + file for file in self.FromFiles]

    def grading(self):

        f = open("results.txt", "w")

        os.chdir('./'+self.subdirName) 
        filenames = os.listdir(".")
 
        for filename in filenames:
            # include - in lab7, filename is graph-courses.txt
            #m=re.search('([a-zA-Z_]+)(_\d+)(_\d+_)([a-zA-Z_0-9-]+)(.+)', filename)
            # do not include - in the name, some names are like filename-1.py
            if os.path.isdir(filename):
                student_name = filename

                # copy files
                for copyfrom,copyto in zip(self.FromFiles,self.ToFiles):
                    # modify labs to hw or exam if needed 
                    copy(self.assignmentPath + 'labs/' + self.AssignmentName + '/' + copyfrom, student_name + '/' + copyto)
                    #copy('../../CMPT306/homework/'+self.AssignmentName+'/'+copyfrom, student_name+'/'+copyto)
                    #copy('../../CMPT306/exam/'+self.AssignmentName+'/'+copyfrom, student_name+'/'+copyto)

                # copy run.bat
                copy('../run.bat', student_name+'/run.bat')
 
                os.chdir(filename)
                
                os.system('echo ========================== >> ../../results.txt')
                os.system('echo %s >> ../../results.txt'%filename)

                os.chmod('run.bat', 0o777)
                #os.system('./run.bat >> ../../grading_files/results.txt')
                # &>>, 2>&1 for saving output of unittest of python
                os.system('./run.bat >> ../../results.txt 2>&1')
                #os.system('rm *.class')
                os.chdir('..')

        f.close()

if __name__ == "__main__":
    
    config = autograder.config()
    settings = config.get()

    obj = grading(settings)
    obj.grading()

    





