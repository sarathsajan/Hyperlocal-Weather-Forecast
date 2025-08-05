import numpy as np
import cv2
import urllib.request
from datetime import datetime, timedelta
from multiprocessing import Pool

days = 1
start_delta = 60 * 60 * 24 * days
init_datetime = datetime(2025,8,5,19,0,0) - timedelta(seconds=start_delta)

def get_map(curr_delta):
    dynamic_time = init_datetime + timedelta(seconds=curr_delta)
    dynamic_time_string = dynamic_time.strftime("%Y_%m_%d_%H_%M_%S")
    try:
        req = urllib.request.urlopen(f"http://117.221.70.132/dwr/archive/MAXZ/maxz_kochi_weather_{dynamic_time_string}_dsfimdb_kochi_maxz_000.gif")
        image_np_array = np.asarray(bytearray(req.read()), dtype=np.uint8)
        cv2_image = cv2.imdecode(image_np_array, cv2.IMREAD_COLOR)
        if cv2_image is not None:
            cv2.imwrite(f'maxz_image_archive/maxz_kochi_weather_{dynamic_time_string}.png', cv2_image)
            print(f'for datetime {dynamic_time_string} : maxz_image_archive/maxz_kochi_weather_{dynamic_time_string}.png')
        else:
            print(f"for datetime {dynamic_time_string} : Failed to decode image.")
    except Exception as e:
        # print(f"for datetime {dynamic_time_string} : Error downloading image: {e}")
        pass

with Pool() as p:
    p.map(get_map, range(start_delta))

print("DONE")