import os, sys

filelist = []
internallist = []
externallist = []

def main():
    #getting filename in directory
    folderPath = sys.argv[1]
    projectname = folderPath.rsplit("/",1)[0]
    for subdir, dirs, files in os.walk(folderPath):
        for file in files:
            if file.endswith(".rb"):
                filelist.append(subdir + os.sep + file)

    #reading each file and find dependency
    for file in filelist:
        with open(file) as fp:
            for line in fp:
                if "require" in line:
                    #print(line)
                    param = finddepword(line)
                    if param is not "":
                        depfile = finddependencyfile(param,file)
                        if depfile is "external":
                            externallist.append(file + ":/External/" + param + ".rb:required_external")
                        else:
                            internallist.append(file + ":" + depfile + ":require_internal")
    #writing output files
    #writefile(projectname)
    
def finddepword(line):
    #get dependent filename
    if "'" in line:
        param = line.split("'",1)[1]
        param = param.split("'",1)[0]
        return param
    if '"' in line:
        param = line.split('"',1)[1]
        param = param.split('"',1)[0]
        return param
    return ""

def finddependencyfile(depword,file):
    #determine whether it is external or internal
    path = file.rsplit("/",1)[0]
    depfile = path + "/" + depword + ".rb"
    if depfile in filelist:
        return depfile
    else:
        return "external"

def writefile(projectname):
    #internal dependency list
    with open(projectname + "_internal_deps.list","w") as fp:
        for line in internallist:
            fp.write(line+"\n")

    #external dependency list
    with open(projectname + "_external_deps.list","w") as fp:
        for line in externallist:
            fp.write(line+"\n")

if __name__ == '__main__':
   main()
