#!/usr/bin/python
from sys import argv
import zbar
import MySQLdb

try:
    db = MySQLdb.connect("localhost",port=3306, user="root", passwd="x")
    cursor = db.cursor()
    query = ("use regist;")
    cursor.execute(query)
    print 'terhubung database'
    print 'waiting...'

except MySQLdb.OperationalError:
    print 'tidak terhubung database'


# create a Processor
proc = zbar.Processor()

# configure the Processor
proc.parse_config('enable')

# initialize the Processor
device = '/dev/video0'
if len(argv) > 1:
    device = argv[1]
proc.init(device)
print 'Your camera is ready!'

# setup a callback
def my_handler(proc, image, closure):
    # extract results
    for symbol in image.symbols:
        'select nim from maba ;'
        cursor.execute ("select nim from maba ;")
        nim = cursor.fetchall()
        print nim
        for i in nim:
            if symbol.data in i[0]:
                cursor.execute ("select absen from maba where nim='{}';".format(symbol.data))
                absen = cursor.fetchall()[0][0]
                print absen
                if absen != 1:
                    print i[0]
                    print "ada"
                    "update maba  set absen='xx' where nim='11';"
                    sql = cursor.execute("UPDATE  {} SET {}='{}' where {} = '{}';".format("maba","absen","1","nim",symbol.data))
                    db.commit()
                    print "Successfully! You "+symbol.data+" absen now!"
                    print "\n"
                    break
            else:
                print "tidak ada"
                print "\n"
                continue


proc.set_data_handler(my_handler)

# enable the preview window
proc.visible = True

# initiate scanning
proc.active = True
try:
    # keep scanning until user provides key/mouse input
    proc.user_wait()
except zbar.WindowClosed, e:
    pass

