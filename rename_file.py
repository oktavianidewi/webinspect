import os, sys

directory = "foodgroups"
# directory = "piBconstitutionalpatriot"
# f = open( os.path.join(directory, "about_109151809438074.html") )
# print f

# os.rename('oktaviani', 'oktaviani1')

for root, dirs, files in os.walk(directory):
    # print "files : ", files
    # rename dir
    """
    for dirname in dirs:
        spaceexist = '\r\n' in dirname
        # print spaceexist
        # if spaceexist:
        try:
            path = os.path.join(directory, dirname)
            target = os.path.join(directory, dirname.replace('\r\n','') )
            os.rename(path, target)
        except OSError:
            pass

    print "dirs : ", dirs
    # rename file
    """


    for name in files:
        file_path_raw = root + '/' + name
        spaceexist = '\r\n' in name
        if spaceexist:
            path = os.path.join(root, name)
            target = os.path.join(root, name.replace('\r\n','') )
            os.rename(path, target)
        print file_path_raw
