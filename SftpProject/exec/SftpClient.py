import os, getpass, posixpath
from shutil import rmtree
from stat import S_ISDIR
import signal
from driver import *

TIMEOUT = 80 #waits for 80 seconds for timeout


options = ["Type help to print options", 
           "Type listdir to list files on remote directory", 
           "Type cd to change directory", 
           "Type getfile to download a file", 
           "Type seeya to logout", 
           "Type getfiles to download multiple files", 
           "Type listloc to list local directory",
           "Type putfile to upload a file", 
           "Type putfiles to upload multiple files",
           "Type createdir to create a directory on remote server",
           "Type deletefile to delete a file on server", 
           "Type modperm to change file permissions on server", 
           "Type renremo to rename file on server",
           "Type renloc to rename file on local machine", 
           "Type cpremo to copy directories on server",
           "Type deletedir to delete directory from server"]




    


"""
Author: Faiyazthulla Shaik 

Signal handler is used to handle keyboard interrupt CTRL+c. 
When the user presses the CTRL+c on the console, the program terminates automatically.
"""
def signal_handle(signum, frame):
    print("You wished to close the client by pressing CTRL+c. \n Until next time")
    exit()

signal.signal(signal.SIGINT, signal_handle)
                






"""
Author: Faiyazthulla Shaik

Below function is used to upload the multiple files to the server.
Input: Files path on the local machine and the name of the files.
Output: Function returns true or false. True means successful upload and false means unsuccesful upload.
"""
def putfiles(filepath, filesnames, sftpconn):    
    for i in filesnames:
        if os.path.isfile(i) and os.path.exists(i):
            print(f"Uploading file:{i}")
            sftpconn.put(filepath+"/"+i,confirm=True, preserve_mtime=False)            
            if sftpconn.exists(i):
                print("File Uploaded Successfully")
            else:
                print("File Upload Failed")
        else:
            print(f"Filename you entered does not exists.\n Please try again")






"""
Author: Faiyazthulla Shaik

Below functions is used to list the directories of the SFTP server in the pwd.
The output of the function is similar to listdir command on linux.
"""    
def toListDir(sftpconn):
    for info in sftpconn.listdir_attr(remotepath='.'):
        print(info)    






"""
Author: Faiyazthulla Shaik

Below function is used to download the file from the SFTP Server.
Input: Name of the file that needs to be downloaded.
"""
def getFileOnSftp(sftpconn):
    print("Enter the name of the file with extension from the current directory")
    filename = input()
    if sftpconn.isfile(filename):
        print(f"Downloading file:{filename} from current directory")
        if getfile(filename,sftpconn):
            print("Downloaded successfully")
        else:
            print("Download failed. \n retrying to download automatically")
            if getfile(filename):
                print("Downloaded successfully")
            else:
                print("Download failed again.\n Please try again after some time")
    else:
        print(f"Filename you entered does not exist.\n Please try again")





"""
Author: Faiyazthulla Shaik

Below function is used to download the multiple files from the server at the same time.
"""
def toDownloadMultipleFiles(sftpconn):
    print("enter the file names from the current directory with space")                
    files = input()
    fileslist = files.split()              
    for i in fileslist:
        if sftpconn.isfile(i) and sftpconn.exists(i):
            print(f"Downloading file:{i} from current directory")
            if getfile(i,sftpconn):
                print("Downloaded successfully")
            else:
                print("Download failed.")
        else:
            print(f"Filename you entered does not exists.\n Please try again")






"""
Author: Faiyazthulla Shaik

Below function is used to upload a single file on to the SFTP Server.
"""
def toUploadFile(sftpconn):
    print("Enter the path on local directory where the file is present")
    filepath = input()
    if os.path.isdir(filepath):
        print("Enter the filename from the mentioned directory")
        filename = input()
        if putfile(filepath,filename,sftpconn):
            print("File uploaded successfully")
        else:
            print("File upload failed.")







"""
Author: Faiyazthulla Shaik

Below function is used to create a diectory on the SFTP Server.
"""
def toCreateDirectory(sftpconn):
    print("Enter the name of the directory you want to create :")
    newdir = input() 
    if sftpconn.isdir(newdir) and sftpconn.exists(newdir):
        print("The directory name you entered already exists. Try again:")
    else:
        print(f"Creating a new directory with name: {newdir}")
        sftpconn.mkdir(newdir,mode=777)
        if sftpconn.exists(newdir):
            print(f"Created a new directory with name: {newdir} successfully")
            for info in sftpconn.listdir_attr(remotepath='.'):
                print(info)
        else:
            print(f"an error occured while craeting {newdir} creating")






"""
Author: Faiyazthulla Shaik.

Below function is used to delte a directory form the SFTP server.
"""
def toDeleteDir(sftpconn):
    print("Enter directory name to delete from server")
    deldir = input()
    level=0
    if sftpconn.exists(deldir):
        print("Deleting the directory you entered...")
        for contents in sftpconn.listdir_attr(deldir):
            rempath = posixpath.join(deldir, contents.filename)
            if S_ISDIR(contents.st_mode):
                rmtree(sftpconn, rempath, level=(level + 1))
            else:
                rempath = posixpath.join(deldir, contents.filename)
                print('removing %s%s' % ('    ' * level, rempath))
                sftpconn.remove(rempath)
        sftpconn.rmdir(deldir)
        if sftpconn.exists(deldir):
            print("Deleting folder failed. Please try again")
        else:
            print("Deleted the directory successfully")
    else:
        print(f"The directory name you entered does not exist")







"""
Author: Faiyazthulla Shaik

Below function is used to rename the file on the local machine.
"""
def toRenameOnLocal():
    print("Enter the filename you want to rename on the local machine")
    renlfname= input()
    if os.path.isfile(renlfname) and os.path.exists(renlfname):
        print("Enter the new name you want for the file")
        newrenlfname= input()
        if os.path.isfile(newrenlfname) and os.path.exists(newrenlfname):
            print("the new filename already exists")
        else:
            os.rename(renlfname, newrenlfname)
            if os.path.isfile(newrenlfname) and os.path.exists(newrenlfname):
                print("File renamed successfully") 
            else:
                print("File rename unsuccessful. Please try again")
    else:
        print("The filename you entered dooes not exist")



              



"""
Author: Faiyazthulla Shaik

Below function is used to store the username, password and servername details into a file named savecon.log
Initially it will check whether the savecon.log file exists or not. 
If file doesn't exists it will create a new file as savecon.log
"""
def savecon(hname,user,passd):
    while(True):
        if os.path.isfile("savecon.log"):
            savefile = os.path.join(os.getcwd(),"savecon.log")
            save = open(savefile, "a")
            save.write("\nConnection:succesful\n")
            save.write(f"host:{hname}\n")
            save.write(f"username:{user}\n")
            save.write(f"pass:{passd}\n")
            break
        else:
            save=open("savecon.log", "x")
            continue







"""
Author: Faiyazthulla Shaik

Below function will fectch the file from the SFTP Server and download it into the local folder.
"""
def getfile(filename,sftpconn):    
    try:
        sftpconn.get(filename, preserve_mtime=True)
    except IOError as e:
        return False
    
    if os.path.exists('./'+filename):
        return True
    else:
        return False


