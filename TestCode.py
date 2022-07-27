import pysftp
from urllib.parse import urlparse
import os
import paramiko


class Sftp:
    def __init__(self, hostname, username, password, port=22):
        """Constructor Method"""
        # Set connection object to None (initial value)
        self.connection = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        """Connects to the sftp server and returns the sftp connection object"""
        try:
            # Get the sftp connection object
            self.connection = pysftp.Connection(
                host=self.hostname,
                username=self.username,
                password=self.password,
                port=self.port,
            )
        except Exception as err:
            raise Exception(err)
        finally:
            print(f"Connected to {self.hostname} as {self.username}.")

    def disconnect(self):
        """Closes the sftp connection"""
        self.connection.close()
        print(f"Disconnected from host {self.hostname}")

    def listdir(self, remote_path):
        """lists all the files and directories in the specified path and returns them"""
        for obj in self.connection.listdir(remote_path):
            yield obj

    def listdir_attr(self, remote_path):
        """lists all the files and directories (with their attributes) in the specified path and returns them"""
        for attr in self.connection.listdir_attr(remote_path):
            yield attr

    def download(self, remote_path, target_local_path):
        """
        Downloads the file from remote sftp server to local.
        Also, by default extracts the file to the specified target_local_path
        """

        try:
            print(
                f"downloading from {self.hostname} as {self.username} [(remote path : {remote_path});(local path: {target_local_path})]"
            )

            # Create the target directory if it does not exist
            path, _ = os.path.split(target_local_path)
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except Exception as err:
                    raise Exception(err)

            # Download from remote sftp server to local
            self.connection.get(remote_path, target_local_path)
            print("download completed")

        except Exception as err:
            raise Exception(err)

    def upload(self, source_local_path, remote_path):
        """
        Uploads the source files from local to the sftp server.
        """

        try:
            print(
                f"uploading to {self.hostname} as {self.username} [(remote path: {remote_path});(source local path: {source_local_path})]"
            )

            # Download file from SFTP
            self.connection.put(source_local_path, remote_path)
            print("upload completed")

        except Exception as err:
            raise Exception(err)

    def mkdir_p(sftp, remote_directory):
        dir_path = remote_directory
        print("Directory path: "+dir_path)
        for dir_folder in remote_directory.split("/"):
            if dir_folder == "":
                continue
            dir_path += r"/{0}".format(dir_folder)
            try:
                sftp.mkdir(dir_path)
            except IOError:
                sftp.mkdir(dir_path)


if __name__ == "__main__":
    i=0
    while i<=0:
        print("\n")
        print("========================================OPTIONS========================================\n")
        print("1. To connect server. ")
        print("2. List the files on the server. ")
        print("3. Upload the files from local machine. ")
        print("4. Download the files from the server. ")
        print("5. Disconnect from the server. ")
        print("6. List the files on the local machine. ")
        print("7. Download multiple files from server. ")
        print("8. Create a directory on server. ")
        option = input("Please enter your choice:")
        print("\n")

        if(option == "1"):
            sftp_url = os.environ.get("SFTPTOGO_URL")

            if not sftp_url:
                print("First, please set environment variable SFTPTOGO_URL and try again.")
                exit(0)

            parsed_url = urlparse(sftp_url)

            sftp = Sftp(
                hostname=parsed_url.hostname,
                username=parsed_url.username,
                password=parsed_url.password,
            )

            # Connect to SFTP
            sftp.connect()

        if(option == "5"):
            sftp.disconnect()
            exit(0)

        if(option == "3"):
            local_path = input("Please enter the path to upload the file: ")
            remote_path = input("Please enter the path on server, where file needs to be uploaded. Path:")
            sftp.upload(local_path, remote_path)

        if(option == "2"):
            path = input("Please enter the path:")
            print(f"List of files at location {path}:")
            print([f for f in sftp.listdir(path)])

        if(option == "4"):
            local_path = input("Please enter the path of local machine to download the files. Path:")
            remote_path = input("Please enter the remote path from where file needs to be downloaded. Path:")
            sftp.download(remote_path, os.path.join(remote_path, local_path))

        if(option == "6"):
            path = input("Please enter the path on local machine. Path:")
            print(f"List of files at location {path}:")
            print([f for f in os.listdir(path)])

        # This needs to be corrected. 
        if(option == "7"):
            remote_path_option7 = input("Please enter the path to download the mutiple files from server. Path:")
            local_path = input(f"Please enter the path of local machine to download the files. Path:")
            downloadFilesList = []
            files = sftp.listdir(remote_path_option7, local_path)
            for file in files:
                sftp.get(file)
                downloadFilesList.append(file)
                print(file, " was downloaded successfully")
            print("These files were downloades ", downloadFilesList)
        
        if(option == "8"):
            remote_path = input("Please enter the path to where folder needs to be created. Path:")
            directory_name = input("Please directory name that needs to be created. Directory Name:")
            sftp.mkdir_p(remote_path+directory_name)