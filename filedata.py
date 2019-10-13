import os
import sys
import sqlite3

project_folder = 'FileDatabase'

if not project_folder in os.listdir():
    os.makedirs(project_folder, exist_ok=True)

os.chdir(project_folder)
redir= os.getcwd()

if 'filedb.db' not in os.listdir():
    conn = sqlite3.connect('filedb.db')
    curr= conn.cursor()
    curr.execute("CREATE TABLE IF NOT EXISTS filedb_table (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, filename TEXT, data BLOP)")
    conn.commit()
    conn.close()

if 'FilesHere' not in os.listdir():
    os.makedirs('FilesHere',exist_ok=True)

os.chdir('FilesHere')
fildir= os.getcwd()
os.chdir(redir)

conn = sqlite3.connect('filedb.db')
curr= conn.cursor()
curr.execute('SELECT filename FROM filedb_table')
raw_names= curr.fetchall()
clear_names=[]

for i in range(len(raw_names)):
    clear_names.append(raw_names[i][0])

def writetodatabase(file,fildir):
    try:
        filewithpath = fildir+'/'+file
        with open(filewithpath, 'rb') as f1:
            filedata = f1.read()
        with conn:
            curr.execute('''
            INSERT INTO  filedb_table (filename,data) VALUES(?,?)''', (file, filedata))
        print('Successfully recorded ' + file + ' in the database')
        print(' ')

    except:
        print('Failed to record ' + file)

for file in os.listdir(fildir):
    if file not in clear_names:
        print(file)
        writetodatabase(file,fildir)

if not 'RetrievedFiles' in os.listdir():
    os.makedirs('RetrievedFiles')

os.chdir('RetrievedFiles')
ret_dir=os.getcwd()
os.chdir(redir)

def retordel(ret_dir):
    print('------------------------------------------------------------------------------------')
    print('Enter r to retrieve and d to delete or any other key to exit:')
    print('')
    value=0
    usr = input()
    if usr.lower() == 'r':
        value = 'r'

    if usr.lower()== 'd':
        value ='d'

    else:
        with conn:
            conn.execute('VACUUM')

    if (value =='r') or (value == 'd'):
        curr.execute("SELECT id, filename FROM filedb_table")
        filewithid = curr.fetchall()
        idnames =[]
        for files in filewithid:
            idnames.append(files[0])

        for ids in filewithid:
            print(ids)
        print('')
        if value=='r':
            print('Enter ID no. of files (seperated by comma) to retrieve:')
        elif value == 'd':
            print('Enter ID no. of files (seperated by comma) to delete:')

        inp = input()
        inp = inp.split(',')

        for num in inp:
            try:
                int(num)
            except Exception as e:
                print(e, 'Enter integer values seperated by comma.')
                break

            if int(num) in idnames:
                reqdfile = filewithid[idnames.index(int(num))][1]
                if value == 'r':
                    print(reqdfile)
                    curr.execute("SELECT filename, data FROM filedb_table WHERE id = :id", {'id':num})
                    dataret = curr.fetchone()[1]
                    filewithpath= ret_dir+'/'+reqdfile
                    with open (filewithpath, 'wb') as f1:
                        f1.write(dataret)
                    print('Successfully Retrieved ' + reqdfile + ' at ' + ret_dir)
                    print('')
                if value == 'd':
                    with conn:
                        curr.execute("DELETE FROM filedb_table WHERE id = :id", {'id': num})  
                    print('Successfully deleted ' + reqdfile + ' from the database')
                    print('')          
        retordel(ret_dir)

retordel(ret_dir)
conn.close()
