# Store-files-in-Sqlite
This Python 3 script allows to store files and images to store in a sqlite database which is locally created by this script. Stored files in the sqlite database can be deleted and retrieved again also.

# Using the script:

-When the script is first time run using 'python filedata.py' it creates a folder project by the name 'FileDatabase' which again contains two folders 'FilesHere' and 'RetrievedFiles' and also an empty sqlite database by the name filedb.db

-Files and Images which are supposed to be stored in the sqlite database should be copied and placed inside the folder 'FilesHere'. Now when the script is run again files and images which are inside the 'FilesHere' folder are automatically stored inside the database.

- When those stored files are retrieved they all are placed inside 'RetrievedFiles' folder. Retrieving only doesn't delete the data present inside the database. Delete command can be provided from within the script if files are to be deleted.

- The database filedb.db can be copied and can be shared and accessed from other places too. Data are present inside the table filedb_table and stored as blob type. This same script can also be used to retrieve data from the database by placing this database inside the project folder.
