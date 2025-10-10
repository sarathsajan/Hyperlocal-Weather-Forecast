from PIL import Image
import os
import shutil
from time import sleep

def get_single_image_rgb_list(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    img_width, img_height = img.size
    print(f"Image dimensions: {img_width}x{img_height} = {img_width * img_height} pixels")
    single_image_rgb_list = []
    for y in range(img_height):
        row_wise_rgb_list = []
        for x in range(img_width):
            r, g, b = img.getpixel((x, y))
            row_wise_rgb_list.append((r, g, b))
        single_image_rgb_list.append(row_wise_rgb_list)
    return single_image_rgb_list

def get_multi_image_rgb_list(image_folder_path):
    multi_image_rgb_list = []
    for file_name in os.listdir(image_folder_path):
        if file_name.lower().endswith('.png'):
            image_path = os.path.join(image_folder_path, file_name)
            print(f"Processing: {image_path}")
            multi_image_rgb_list.append(get_single_image_rgb_list(image_path))
    print('length of multi image list', len(multi_image_rgb_list))
    print('length of first image in the multi image list', len(multi_image_rgb_list[0]))
    print('length of first row in the first image in the multi image list', len(multi_image_rgb_list[0][0]))
    print('RGB value of first pixel in the first row of the first image in the multi image list', multi_image_rgb_list[0][0][0])
    print('R value of first pixel in the first row of the first image in the multi image list', multi_image_rgb_list[0][0][0][0])
    return multi_image_rgb_list

def get_pixel_rgb_statistical_mode():
    all_image_rgb_list = get_multi_image_rgb_list('..\..\maxz_image_archive')
    final_image_rgb_list = []
    base_map_height = len(all_image_rgb_list[0])
    base_map_width = len(all_image_rgb_list[0][0])
    for row in range(base_map_height):
        row_wise_pixel_rgb_list = []
        for pixel in range(base_map_width):
            single_pixel_rgb_list = []
            for image_item in all_image_rgb_list:
                single_pixel_rgb_list.append(image_item[row][pixel])
            row_wise_pixel_rgb_list.append(max(set(single_pixel_rgb_list), key=single_pixel_rgb_list.count))
        final_image_rgb_list.append(row_wise_pixel_rgb_list)
    print('length of final image list', len(final_image_rgb_list))
    print('length of first row in the final image list', len(final_image_rgb_list[0]))
    print('RGB value of first pixel in the first row of the final image list', final_image_rgb_list[0][0])
    return final_image_rgb_list

def generate_image_with_rgb_values(rgb_values, width, height, output_path):
    print(len(rgb_values), width * height)
    if len(rgb_values) != width * height:
        raise ValueError("The number of RGB values does not match the specified dimensions.")
    img = Image.new('RGB', (width, height))
    img.putdata(rgb_values)
    img.save(output_path)
    print(f"Image saved at {output_path}")

base_map_rgb_matrix = get_pixel_rgb_statistical_mode()
base_map_rgb_flat_list = []
for row in base_map_rgb_matrix:
    for pixel in row:
        base_map_rgb_flat_list.append(pixel)
generate_image_with_rgb_values(base_map_rgb_flat_list, len(base_map_rgb_matrix[0]), len(base_map_rgb_matrix), 'base_map.png')
