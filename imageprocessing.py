import os
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from skimage.transform import resize
from keras.preprocessing.image import load_img

os.chdir('/Users/wigasper/Documents/Python/English Practice')

image = load_img("./RGALI Documents/1.tif", color_mode='grayscale',
                 target_size=None)

image_id = 1

def window_gen(image_in):
    
    segments = 20
    image = image_in
    count = 0

    # tuning value for optimizing window spacing
    spacer_tuning_val = 3
    
    # window height as a factor of window width
    window_height = 2
    
    crop_width = image.width / segments
    crop_height = crop_width * window_height

    while crop_width > 30:
        y = 0 
        for horizontal in tqdm(range(0, segments * spacer_tuning_val)):   
            x = 0
            for vertical in range(0, segments * spacer_tuning_val):
                image_out = image.crop(box=(x, y, x + crop_width,
                                            y + crop_height))
                image_out = np.array(image_out)
                
                # increase contrast. These values may need to be optimized
                image_out[image_out < 100.0] = 1.0
                image_out[image_out > 180.0] = 255.0

                # output image if it is not all white or all black
                if image_out.mean() > 115.0 and image_out.mean() < 250.0:
                    image_out = image_out / 255.0
                    image_out = resize(image_out, (100, 50))
                    window_id = "".join([str(image_id).zfill(4), 
                                         str(count).zfill(5)])
    
                    # output: [image as np array, ID, x min, x max, y min,
                    #           y max]
                    yield [image_out, window_id, int(x), 
                              int(x + crop_width), int(y), 
                              int(y + crop_height)]
                    
                    count += 1
                x += crop_width / spacer_tuning_val
            y += crop_height / spacer_tuning_val
        
        segments = int(segments * 1.25)
        crop_width = image.width / segments
        crop_height = crop_width * window_height


# to save images:
gen = window_gen(image)
for window in gen:
    plt.imsave("./crops/{}.jpg".format(window[1]), window[0])

