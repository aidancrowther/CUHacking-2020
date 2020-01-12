import os
from check_for_butterfly import getClass
from shutil import copyfile

src = "Dataset/"
path = "Data/"
dirs = os.listdir( src )

for species in dirs:
    images = os.listdir(src+species)
    sure = 0
    unsure = 0
    bad = 0
    for each in images:
        res = getClass(src+species+'/'+each)
        if res is not None:
            if res[0] > 0.85:
                if not os.path.exists(path+species+'/clean/'):
                    os.makedirs(path+species+'/clean/')
                copyfile(src+species+'/'+each, path+species+'/clean/'+str(sure)+'.png')
                sure += 1
            elif res[0] > 0.6:
                if not os.path.exists(path+species+'/unsure/'):
                    os.makedirs(path+species+'/unsure/')
                copyfile(src+species+'/'+each, path+species+'/unsure/'+str(unsure)+'.png')
                unsure += 1
            else:
                if not os.path.exists(path+species+'/bad/'):
                    os.makedirs(path+species+'/bad/')
                copyfile(src+species+'/'+each, path+species+'/bad/'+str(bad)+'.png')
                bad += 1

        res = None
