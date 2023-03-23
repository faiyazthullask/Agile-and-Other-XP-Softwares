from SftpClient import *
import pysftp

"""
Author: Faiyazthulla Shaik

Below function is called from the driver.py. 
The function checks whether the savecon.log file was present or not. 
If the file is present, it will ask whether the user wants to use the last used credits. 
If the user response is yes, the code will establish connection to the Sftp server using the saved details which are fetched from the savecon.log file. 
If the user response is no, the progarm asks the user to enter the server name, username and password.
"""
def ask():
    if os.path.exists("savecon.log"):
        print("Would you like to use your previously saved login details?(y/n)")
        descision=input()
        if descision == 'y':
            response=usesavecon(3)
            print(f"Saved credentials: {response[0]},{response[1]}")
            connect(response[0],response[1],response[2])
        else:
            credos=creds()
            connect(credos[0],credos[1],credos[2])
    else:
        credos=creds()
        connect(credos[0],credos[1],credos[2])


"""
Author:Chaitanya Boyapati & Faiyazthulla Shaik
Below function acts as a driver for selecting the options.
"""
def FileOptions(sftpconn):
        global login_user, working_dir
        displayOption()
       
        while(True):            
            print(f"you are now in the following directory :{sftpconn.pwd}")
            print("Enter your choice:")
            choice = input()            
            if choice.lower() == "help":
                displayOption()
                            
            if choice.lower() == "listdir":
                toListDir(sftpconn)
                
            if choice.lower() == "cd":
                toChangeDirectory(sftpconn)
            
            if choice.lower() == "getfile":                
                getFileOnSftp(sftpconn)
                        
            if choice.lower() == "logout":
                toLogout(sftpconn)
            
            if choice.lower() == "getfiles":
                toDownloadMultipleFiles(sftpconn)
                    
            if choice.lower() == "listloc":
                toListDirectories()
                
            if choice.lower() == "putfile":
                toUploadFile(sftpconn)
                    
            if choice.lower() == "putfiles":
                toUploadMultipleFiles(sftpconn)
            
            if choice.lower() == "createdir":
                toCreateDirectory(sftpconn)
                        
            if choice.lower() == "deletefile":
                toDeleteFile(sftpconn)
                    
            if choice.lower() == "deletedir":
                toDeleteDir(sftpconn)
            
            if choice.lower() == 'renremo':
                toRenameFile(sftpconn)

            if choice.lower() == "renloc":
                toRenameOnLocal()

            if choice.lower() == "cpremo":
                copyFiles(sftpconn)

            if choice.lower() == "modperm":
                toChangePermissions(sftpconn)