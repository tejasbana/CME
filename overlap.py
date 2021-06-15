from PIL import Image
import numpy as np
from PIL import ImageOps
def overlap_camo(filtered,cropped,camo_pattern):
    pil_filtered = Image.fromarray(filtered)
    pil_cropped = Image.fromarray(cropped)
    pil_camo = Image.fromarray(np.array(camo_pattern))
    width, height = pil_filtered.size
    #print(width , height)
    pil_camo = pil_camo.resize((100,100))
    camo_w, camo_h = pil_camo.size
    #print(camo_w, camo_h)
    #print(np.ceil(width/camo_w),np.ceil(height/camo_h))
    rot_array = np.random.randint(0,4,(int(np.ceil(width/camo_w)),int(np.ceil(height/camo_h))))
    #print(rot_array)
    prev_angle_mult = rot_array[0][0]
    for j in range(height):
      for r in range(width):
        rgb_values = pil_filtered.getpixel((r,j))
        if 0 in rgb_values:
          l = r%camo_w
          k = j%camo_h
          angle_mult = rot_array[int(r/camo_w)][int(j/camo_h)]
          #angle_mult = random.randint(0,4)
          #pil_filtered.putpixel( (r,j),pil_camo.getpixel((l,k)))
          pil_filtered.putpixel( (r,j), pil_camo.rotate(90*angle_mult).getpixel((l,k)))
          prev_angle_mult = angle_mult
    gray_image = ImageOps.grayscale(pil_cropped).convert("RGB")
    print(gray_image.mode,pil_filtered.mode)
    pil_filtered = Image.blend(pil_filtered,gray_image,alpha = .3)
    return pil_filtered