import os
from sys import *
import hashlib
import time
import schedule


def ProcessDisplay(log_dir="Deleted_Logs"):
    listprocess = []

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    separator = "_" * 80
    log_path = os.path.join(log_dir, "SystemLog_by_RD %s .log" % time.strftime('%Y-%m-%d %H-%M-%S'))
    with open(log_path, 'w') as f:
        f.write(separator + "\n")
        f.write("Ritesh System Process Logger: " + time.ctime() + "\n")
        f.write(separator + "\n")

        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                
                vms = proc.memory_info().vms / (1024 * 1024)
                pinfo['vms'] = vms
                listprocess.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        for element in listprocess:
            f.write("%s\n" % element)


def DeleteFiles(dict1, log_dir="Deleted_Logs"):
    results = list(filter(lambda X: len(X) > 1, dict1.values()))

    icnt = 0

    if len(results) > 0:
        separator = "_" * 80
        log_path = os.path.join(log_dir, "DeletedFilesLog_by_RD %s .log" % time.strftime('%Y-%m-%d %H-%M-%S'))
        with open(log_path, 'w') as f:
            f.write(separator + "\n")
            f.write("Ritesh Deleted Files Logger: " + time.ctime() + "\n")
            f.write(separator + "\n")

            for result in results:
                # Keep the first occurrence of the file
                original_file = result[0]
                for subresult in result[1:]:
                    icnt += 1
                    os.remove(subresult)
                    f.write("File deleted: %s\n" % subresult)
                icnt = 0

                # Log that duplicates have been removed
                f.write("Duplicates removed for file: %s\n" % original_file)
    else:
        print("No duplicate files found.")


def hashfile(path,blocksize = 1024):
    afile = open(path,'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)

    while len(buf)>0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()

    return hasher.hexdigest()

def findDup(path):
    flag = os.path.isabs(path)

    if flag == False:
        path = os.path.abspath(path)

    exists = os.path.isdir(path)

    dups = {}

    if exists:
        for dirName,subdirs,fileList in os.walk(path):
            print("Current folder is : "+ dirName)
            print("")
            for filen in fileList:
                path = os.path.join(dirName, filen)
                file_hash = hashfile(path)

                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]
        return dups
    else:
        print("Invalid path")

def printResults(dict1):
    results = list(filter(lambda X: len(X) > 1,dict1.values()))

    if len(results) > 0:
        print("Duplicate Found")
        print("")
        print("The following files are duplicate")
        for result in results:
            for subresult in result:
                print('\t\t %s' % subresult)
                print("")
            #print("Do you want to delete this files..?")
            print("Files Deleted Successfully...")
    
            

def main():
    print("______Project by Ritesh Deomore______")
    print("")

    print("Aplication name: " + argv[0])
    print("")

    if (len(argv) != 2):
        print("Error: Invalid number of arguments")
        exit() 

    if (argv[1] == "-h") or (argv == "-H"):
        print("This script is used to travers specific directory and checks the duplicate files found or not ")
        exit()

    if (argv[1] == "-u") or (argv == "-U"):
        print("Usage : Application Name AbsolitePath_of_Directory Extension")
        exit()

    try:
        arr = {}
        startTime = time.time()
        arr = findDup(argv[1])
        printResults(arr)
        DeleteFiles(arr, log_dir=argv[1])
        endTime = time.time()

        print('Took %s seconds to evaluate.' % (endTime - startTime))

    except ValueError:
        print("Error : Invalid datatype of input")

    except Exception as E:
        print("Error : Invalid input",E)

if __name__ == '__main__':
    main()
