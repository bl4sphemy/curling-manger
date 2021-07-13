# curling-manger
PyQT5 based Curling League Manger App

To run this application you need to start launch the MainWindow.py file located in the qt_windows directory. 

My setup.py file can be used to generate a tar.gz archive for distribution. I ran it using 'python3 setup.py sdist'
which created the dist/curling-manager-1.0.0.tar.gz archive. 

The import button on the mainWindow requires a league to be added and selescted in the list widget. If you try to 
add import without it you wil get an index error as the import requires a league name and filename. 

Import File: test_database2.csv

Export File: test_outdb.csv

The sessinos are persistent from window to window. The only issue seems to be the 'Load' method. I was working on that
before the deadline. 

