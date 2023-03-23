# Code Revision Review

The code was modified by Faiyazthulla Shaik and Chaitanya Boyapati as part of course Code revison and review.
The previous version project contains all the code in a single file and there were few bugs in the funcationalities.
And another drawback in the previous version is most of the code was written in a single function.

Changes made by Chaitanya Boyapati & Faiyazthulla Shaik:

- We splitted the code into different functions and each function is related to a single funcationality.
- In the previous version no comments were written. We added comments to each funcationality clearly to improve the readability and maintainability of code.
- We tried to implement the unit test for each funcationality but due to time containt we are unable to do so.
- Added LICENCE to the project.
- Implemented almost everything as mentioned in the proposal.

The original project can be viewed at: https://github.com/sandeepsingamaneni/Agile-SFTPClient/

The text below the line 19 is from the old README file.

---

# AGILE & OTHER XP SOFTWARES

This project was developed for the course CS 510 MDRN AGILE & OTHR XP SOFTWARES at PSU. It was developed under the guidance of professor "Christopher Gilmore".

## Project Environment

This project was developed using

- Python
- pysftp
- paramiko
- unittest(unit testing framework)
- WinSCP (Remote SFTP Server)

## How to execute the application

The executable file "SFTP-Client.bat" is present in the "\SftpProject\exec". By double clicking it will start the execution.

## Basic Features

1.  Log into remote ftp server
2.  List directories & files on remote server
3.  List directories & files on local machine
4.  Getting file from remote server
5.  Getting multiple files from remote server
6.  Putting file onto remote server
7.  Putting multiple files on remote server
8.  Create directory on remote server
9.  Delete file from remote server
10. Change permissions on remote server
11. Copy directories on remote server
12. Delete directories on remote server
13. Rename file on remote server
14. Rename file on local machine
15. Log off from remote server
16. Save connection information
17. Use saved connection information to connect

## Team Members

1.  Chaitanya Boyapati
2.  Faiyazthulla Shaik
3.  Lahari Kattepalli
4.  Sandeep Singamaneni
5.  Rachana Bolla

## References

1.  https://docs.python.org/3/library/unittest.html
2.  https://pysftp.readthedocs.io/en/release_0.2.9/
3.  https://www.pcwdld.com/how-to-access-sftp-server-in-python
