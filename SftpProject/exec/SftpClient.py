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
Author: Chaitanya Boyapati

Below function prints the available options on console. 
"""
def displayOption():
    print("\n*******************************************************************************************************************")
    for option in options:
        print(option)
    print("*******************************************************************************************************************\n")
    


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
Author: Chaitanya Boyapati

Below function is used to upload the file to the server.
Input: Name of the file that needs to be uploaded.
Output: Function returns true or false. True means successful upload and false means unsuccesful upload.
"""
def putfile(filepath,filename,sftpconn):
    try:
        sftpconn.put(filepath+"/"+filename,confirm=True, preserve_mtime=False)
    except IOError as e:
        return False
        
    if sftpconn.exists(filepath+"/"+filename):
        return True
    else:
        return False



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
Author: Chaitanya Boyapati

Below function is used to change the permission on the file or directory.
"""
def add(up,gp,op):
    print("assigning permissions")
    return int(up+gp+op)



"""
Author: Faiyazthulla Shaik

Below functions is used to list the directories of the SFTP server in the pwd.
The output of the function is similar to listdir command on linux.
"""    
def toListDir(sftpconn):
    for info in sftpconn.listdir_attr(remotepath='.'):
        print(info)    



"""
Author: Chaitanya Boyapati

Below function is used to change the present working director.
"""
def toChangeDirectory(sftpconn):
    print("Enter name of directory :")
    working_dir = input()
    print(working_dir)
    try:    
        if sftpconn.isdir(working_dir):
            sftpconn.cwd(working_dir)
        else:
            print("The name of the directory you entered is incorrect. Please try again")
    except Exception as e:
            print("An error occured while changing directory:",e)



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
Author: Chaitanya Boyapati

Below function is used to logout from the SFTP Server. 
Input: 'y' or 'n'. y means logout from the server.
"""
def toLogout(sftpconn):
    print("Are you sure to logout?(y/n)")
    logout = input()
    if logout == 'y':
        sftpconn.close()
        exit()
    elif logout == 'n':
        print("Selected No!!")


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
Author: Chaitanya Boyapati

Below function is used to print the folder names in the pwd of SFTP server. 
"""
def toListDirectories():
    print("listingfiles and folders in current directory")
    for paths in os.scandir(os.getcwd()):
        print(paths.name)



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
Author: Chaitanya Boyapati

Below function is used to upload multiple files at same time on to the SFTP Server.
"""
def toUploadMultipleFiles(sftpconn):
    print("Enter the file names from the current directory with space")
    files = input()
    filepath = '.'
    filesnames = files.split()
    putfiles(filepath, filesnames, sftpconn)
    print("Files upload complete")



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
Author: Chaitanya Boyapati

Below function is used to delete a file from the SFTP Server.
"""
def toDeleteFile(sftpconn):
    print("Enter file name to delete from server")
    delfname = input()                
    if sftpconn.isfile(delfname) and sftpconn.exists(delfname):
        print("Deleting the file you entered...")
        sftpconn.remove(delfname)
        if sftpconn.exists(delfname):
            print("Deleting file failed. Please try again")
        else:
            print("Deleted the file successfully")
    else:
        print(f"The file name you entered does not exist")



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
Author: Chaitanya Boyapati

Below function is used to rename the filename on the SFTP Server. 
"""
def toRenameFile(sftpconn):
    print("Enter the filename you want to rename on the server")
    renrfname= input()
    if sftpconn.isfile(renrfname) and sftpconn.exists(renrfname):
        print("Enter the new name you want for the file")
        newrenrfname= input()
        if sftpconn.isfile(newrenrfname) and sftpconn.exists(newrenrfname):
            print("the new filename already exists")
        else:
            sftpconn.rename(renrfname, newrenrfname)
            if sftpconn.isfile(newrenrfname) and sftpconn.exists(newrenrfname):
                print("File renamed successfully") 
            else:
                print("File rename unsuccessful. Please try again")
    else:
        print("The filename you entered dooes not exist")



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
Author: Chaitanya Boyapati

Below function is used to copy the files from one directory to another on a SFTP Server.
"""
def copyFiles(sftpconn):
    print("Enter the directory you want to copy:")
    remotesrc= input()
    if sftpconn.isdir(remotesrc):
        print("Enter the directory you want copy to:")
        remotedest= input()
        if sftpconn.exists(remotedest):
            print(f"the directory you entered already exists.")
        else:
            print(f"Copy the directory {remotesrc} to {remotedest}")                        
            comm = 'cp -R'+' '+remotesrc + ' ' +remotedest
            try:
                print(sftpconn.execute(comm))
            except Exception as e:
                print(f"There was an erroe while copying directories. {e} \n Please Try again")
    else:
        print("Enter the directory does not exist:")                



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
Author: Chaitanya Boyapati

Below function will check whether the savecon.log file exists or not. 
If file exists, it will read the file and return the hostname, username and password.\
If file doesn't exits, it will print the message on the console that the file doesn't exists.
"""           
def usesavecon(num):
    if os.path.exists("savecon.log"):
        savefile = os.path.join(os.getcwd(),"savecon.log")
        save = open(savefile, "r")
        credlines= save.readlines()
        credline=credlines[-num:]
        credi = dict(cred.rstrip("\n").split(':') for cred in credline)
        hname=credi.get("host")
        user=credi.get("username")
        passd=credi.get("pass")
        
        return hname,user,passd 
    else:
        print("no previous connection information available")
        creds()



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


"""
Author: Chaitanya Boyapati

Below function is used to change the permission of the folder or file.
"""
def toChangePermissions(sftpconn):
    uperm =7
    gperm =7
    operm =7                
    print("Enter the filename/foldername you want to change permissions")                
    permfile = input()           
    if sftpconn.isfile(permfile) or sftpconn.isdir(permfile) and sftpconn.exists(permfile):
        print("Set user permissions to the file/folder by answering the following questions \n NOTE: by default the permissions are set to read,write and execute")                        
        print("Do you want user to have read permissions? y/n")
        uread = input().lower()
        if uread == 'y':
            perm=4
        elif uread == 'n':
            uperm = 0
                        
        print("Do you want user to have write permissions? y/n")
        uwrite = input().lower()
        if uwrite == 'y':
            uperm = uperm+2
        elif uwrite == 'n':
            uperm = uperm+0
                           
        print("Do you want user to have execute permissions? y/n")
        uexecute = input().lower()
        if uexecute == 'y':
            uperm = uperm+1
        elif uexecute == 'n':
            uperm =uperm+0
                        
        print(f"user permission chmod {permfile} is {uperm}")                        
        print("Set group permissions to the file by answering the following questions \n NOTE: by default the permissions are set to read,write and execute")                        
        print("Do you want group to have read permissions? y/n")
        gread=input().lower()
        if gread == 'y':
            gperm=4
        elif gread == 'n':
            gperm = 0
                        
        print("Do you want group to have write permissions? y/n")
        gwrite = input().lower()
        if gwrite == 'y':
            gperm = gperm+2
        elif gwrite == 'n':
            gperm = gperm+0
                           
        print("Do you want group to have execute permissions? y/n")
        gexecute = input().lower()
        if gexecute == 'y':
            gperm = gperm+1
        elif gexecute == 'n':
            gperm =gperm+0                            
                            
        print("Set others permissions to the file by answering the following questions \n NOTE: by default the permissions are set to read,write and execute")
        print("Do you want others to have read permissions? y/n")
        oread =input().lower()
        if oread == 'y':
            operm=4
        elif oread == 'n':
            operm = 0
                        
        print("Do you want others to have write permissions? y/n")
        owrite = input().lower()                        
        if owrite == 'y':
            operm = operm+2
        elif owrite == 'n':
            operm = operm+0
                           
        print("Do you want others to have execute permissions? y/n")
        oexecute = input().lower()
        if oexecute == 'y':
            operm = operm+1
        elif oexecute == 'n':
            operm =operm+0
                            
        print("Changing file permissions as per permissions set above...")
        finalmod = add(str(uperm),str(gperm), str(operm))
        print(finalmod, type(finalmod))
        try:
            sftpconn.chmod(permfile, finalmod)
            print("Changed file permissions successfully")
        except IOError as e:
            print("Error while assigning permissions. Verify if the file/folder still exists on the server")
    else:
        print("file/folder name you enetered does not exist. Please try again")