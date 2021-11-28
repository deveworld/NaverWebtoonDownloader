import glob
import os
from PIL import Image

def ConvertImage(image_key,image_value):
    
    im = Image.open(image_key+'-'+str(i)+'.jpg')
    print('Get '+image_key+'-'+str(i)+'.jpg')

    print('[Image Convert] Start Change image to out/'+image_key+'.png')

    im.save('out//'+image_key+'.png')
    
if __name__ == '__main__' :
    
    print('[Image Convert] Start Changing Images')
    target_dir = './'
    files = glob.glob(target_dir + '*.jpg')

    name_list = {} 

    # Make Directory
    
    try:
        if not(os.path.isdir('out')):
            os.makedirs(os.path.join('out'))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('[Image Convert] Failed to create directory.')
            raise

    for f in files:
        name = f.split('\\')[1]
        key = name.split('-')[0]
        value = name.split('-')[1].split('.')[0]

        if key in name_list.keys():
            name_list[key].append(int(value))
        else:
            name_list[key] = [int(value)]

        name_list[key].sort()
    
    for key,value in name_list.items():
    	if len(value) == 1:
        	ConvertImage(key,value)
    
    print('[Image Convert] Complete Changing Images')