import sqlite3

conn = sqlite3.connect('orgs.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1]
    org = email.split('@')[1]
    cur.execute('SELECT count FROM Counts WHERE org = ?', (org, ))
    try:
        count = cur.fetchone()[0]
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org, ))
    except:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org, ))

conn.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
for row in conn.execute(sqlstr):
    print(row[0], row[1])

conn.close()
