import numpy as np
import cv2
import urllib.request
import pytz
from datetime import datetime, timedelta
from time import sleep


utc = pytz.utc

days = 0.09
start_delta = 60 * 60 * 24 * days
curr_datetime = datetime.now(utc)
init_datetime = curr_datetime - timedelta(seconds=start_delta)

def get_map():
    last_image_datetime = init_datetime - timedelta(seconds=3600)
    for increment_seconds in range(int((curr_datetime - init_datetime).total_seconds())):
        dynamic_time = init_datetime + timedelta(seconds=increment_seconds)
        dynamic_time_string = dynamic_time.strftime("%Y_%m_%d_%H_%M_%S")

        if dynamic_time < last_image_datetime + timedelta(seconds=(60*14)):
            print(f"for datetime {dynamic_time_string} : optimistic skip")
            continue
        
        try:
            req = urllib.request.urlopen(f"http://117.221.70.132/dwr/archive/MAXZ/maxz_kochi_weather_{dynamic_time_string}_dsfimdb_kochi_maxz_000.gif", timeout=20)
            image_np_array = np.asarray(bytearray(req.read()), dtype=np.uint8)
            cv2_image = cv2.imdecode(image_np_array, cv2.IMREAD_COLOR)
            if cv2_image is not None:
                cv2.imwrite(f'maxz_image_archive/maxz_kochi_weather_{dynamic_time_string}.png', cv2_image)
                print(f'for datetime {dynamic_time_string} : maxz_image_archive/maxz_kochi_weather_{dynamic_time_string}.png')
                sleep(5)
                last_image_datetime = dynamic_time
            else:
                print(f"for datetime {dynamic_time_string} : Failed to decode image.")
        except Exception as e:
            print(f"for datetime {dynamic_time_string} : Error downloading image: {e}")

get_map()
print("DONE")