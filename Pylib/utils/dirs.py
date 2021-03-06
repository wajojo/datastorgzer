from pathlib import Path
import os
from Pylib.utils import files

def isAlive():
    return "Module: _dirs_ it works!"



def createDirectoryTreeDatebased(directory_path):

    new_directory = '/'
    try:
        for dpath in directory_path.split('/'):
            # handle instances of // in string
            if not dpath:
                continue 

            new_directory += dpath + '/'

            if not os.path.isdir(new_directory):
                os.mkdir(new_directory)

        return new_directory

    except PermissionError as e:
        print("Error wth directory!\r\n" +
        "Error number: {0}\r\n".format(e.errno) +
        "Error text: {0}".format(e.strerror))
        return None

def uniqueDirectoryPath(dirpath):
    destination = Path(dirpath)
    if destination.exists():
        return True
    else:
        return False

def getList(dirpath,excluded='None',destpath='/tmp'):

    excluded_directories = 0
    results = []
    directory_quantity = 0
    count = 0
    try:
        entries = Path(dirpath)
        for entry in entries.iterdir():
            #print(entry.name)
            if entry.is_dir():
                count += 1
                print('{}) {}'.format(count,entry))
                directory_quantity += 1

                # count the excluded directories
                if entry.name in excluded:
                    print(f'EXCLUDE: {entry.name}')
                    excluded_directories += 1
                else: 
                    # see modification date 
                    lastmodified = files.getLastModified(entry)
                    #print(lastmodified)


                    ''' determines destination directory in
                    order to organize the folder as a 
                    chronological order '''
                    dest_dir = files.whichDestination(lastmodified)
                    #print(dest_dir)


                    # determines new destination on storage
                    sourcedir = dirpath.replace('/', '_')
                    dstpath = os.path.join(destpath,dest_dir,sourcedir)
                    print('last destination ', dstpath)
                    
                    # verify destination 
                    if not uniqueDirectoryPath(dstpath):
                        print("Destination not found: {} ".format(dstpath))
                        # create a new destination directory
                        createDirectoryCluster(dstpath)
                    else:
                        print("Destination found: {} ".format(dstpath))
    except FileNotFoundError:
            print('[Errno 2] No such file or directory')



    results.append(directory_quantity)
    results.append(excluded_directories)
    return results

def getDirCatalog(dirpath,excluded='None'):

    excluded_directories = 0
    directory_quantity = 0
    files_quantity = 0
    results = []
    last_dir = ''
    subdirectories = []
    excludeddirs = []

    absWorkingDir = os.path.abspath(dirpath)
    
    for folderName, subfolders, filenames in os.walk(dirpath):
        # Mostrar si se quiere
        #print(f'\n< Current folder: {folderName} >') 
   
        for subfolder in subfolders:
            # Mostrar si se quiere
            #print(f'\n* Subfolders de:  {folderName}: {subfolder}')
            
            # I avoid counting the same directory
            if not subfolder  in subdirectories:
                directory_quantity += 1
            
            # memorize the directory already counted
            subdirectories.append(subfolder)
              
            base_folder =  os.path.basename(subfolder)
            #splitted_path = subfolder.split(os.path.sep)
            excludedDirectoryPath = os.path.join(absWorkingDir, subfolder)
            

            # count the excluded directories
            if base_folder in excluded:

                # I avoid counting the same directory
                if not subfolder  in excludeddirs:
                   excluded_directories += 1
                
                # imprime si se quiere 
                #print(f' {subfolder} is EXCLUDED\n')
                #print(f'Path will be excluded: {os.path.abspath(subfolder)}')
                #print(f'Path will be excluded: {base_folder}')

                print("Excluded: " +
                "Directory: {} ".format(base_folder) +
                "at Path: {}".format(subfolder))
                #"at Path: {}".format(excludedDirectoryPath))
 
            #print(f'{os.path.abspath(folders)}')    
            for filename in filenames:
                # Mostrar los archivos. Si se desea
                #print(f'\n_ File inside {folderName} \n \_ {filename}')
                files_quantity += 1
            
    results.append(directory_quantity)
    results.append(excluded_directories)
    results.append(files_quantity)
    return results
