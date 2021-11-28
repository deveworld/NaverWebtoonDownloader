import glob
import os
from PIL import Image


def combineImage(full_width,full_height,image_key,image_list,index):
    canvas = Image.new('RGB', (full_width, full_height), 'white')
    output_height = 0
    
    for im in image_list:
        width, height = im.size
        canvas.paste(im, (0, output_height))
        output_height += height
    
    print('[Image Merger] Start Merge image to out/'+image_key+'.png')

    canvas.save('out//'+image_key+'.png')

def listImage(image_key,image_value):
    full_width, full_height,index = 0, 0, 1
    image_list = []
    
    if len(image_value) != 1:
        for i in image_value:
            im = Image.open(image_key+'-'+str(i)+'.jpg')
            print('Get '+image_key+'-'+str(i)+'.jpg')
            width, height = im.size
        
            if full_height+height > 1000000:
                combineImage(full_width,full_height,image_key,image_list,index)
                index = index + 1
                image_list = []
                full_width, full_height = 0, 0
            
            image_list.append(im)
            full_width = max(full_width, width)
            full_height += height
        
        combineImage(full_width,full_height,image_key,image_list,index)

if __name__ == '__main__' :
    
    print('[Image Merger] Start Combining Images')
    target_dir = './'
    files = glob.glob(target_dir + '*.jpg')

    name_list = {} 

    # Make Directory
    
    try:
        if not(os.path.isdir('out')):
            os.makedirs(os.path.join('out'))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('[Image Merger] Failed to create directory.')
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
        listImage(key,value)
    
    print('[Image Merger] Complete Combining Images')