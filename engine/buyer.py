import json
import random

import mouse
import keyboard
import time
import mss
import numpy as np

from pathlib import Path


def buy_item(x: int, y: int):
    # x = 335
    # y = 748
    # x = 8
    # y = 1
    mouse.move(5 + random.randint(0, 5), 5 + random.randint(0, 5))

    with open(Path(__file__).resolve().parents[1] / "data" / "positions.json", 'r') as f:
        positions = json.load(f)
        dx, dy = positions["faustus_window"][f"({x},{y})"]
        leave_hideout = positions["leave_hideout"]
        faustus_window_logo = positions["faustus_window_logo"]
        menu = positions["menu"]


    status = changed_instance(faustus_window_logo["region"], faustus_window_logo["file_name"])
    if not status:
        print("Loading was too long")
        return
    print("Loading done")

    mouse.move(dx + random.randint(-5, 5), dy + random.randint(-5, 5))

    tries = 0
    while not click_until_bought(dx, dy) and tries < 200:
        keyboard.press("ctrl")
        time.sleep(0.01)
        mouse.click(button="left")
        time.sleep(0.01)
        keyboard.release("ctrl")
        time.sleep(0.02)
        tries += 1
        if tries % 20 == 0:
            print(tries)
    keyboard.press_and_release("i")
    time.sleep(0.01)
    mouse.move(leave_hideout[0] + random.randint(-5, 5), leave_hideout[1] + random.randint(-5, 5), duration=0.01)
    mouse.click(button="left")
    time.sleep(1)
    changed_instance(menu["region"], menu["file_name"])
    print("done")


# def wait_util_enter(file_path: str = r"C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs/Client.txt",
#                     threshold_tries: int = 200) -> bool:
#     with open(file_path, "r") as f:
#         f.seek(0, 2)  # go to end
#         position = f.tell()
#         tries = 0
#         while tries < threshold_tries:
#             f.seek(0, 2)
#             new_position = f.tell()
#             if new_position > position:
#                 f.seek(position)
#                 chunk = f.read(new_position - position)
#                 position = new_position
#                 if "entered" in chunk:
#                     return True
#             tries += 1
#             time.sleep(0.05)
#         else:
#             return False

def changed_instance(region: dict[str,int], file_name: str= 'home', threshold_tries: int = 200) -> bool:
    # if file_name == "trade":
    #     file_name = "faustus_window_logo.npy"
    # else:
    #     file_name = 'menu.npy'
    reference = np.load(Path(__file__).resolve().parents[1] / "data" / file_name)
    tries = 0
    with mss.mss() as sct:
        while tries < threshold_tries:
            img = sct.grab(region)

            frame = np.array(img)
            frame = frame[:, :, :3]

            diff = np.abs(reference.astype(np.int16) - frame.astype(np.int16))
            score = np.mean(diff)

            if score < 2:
                return True
            time.sleep(0.05)
            tries += 1
        else:
            return False


def click_until_bought(x: int, y: int) -> bool:
    with mss.mss() as sct:
        region = {"top": y - 25, "left": x - 25, "width": 50, "height": 50}
        img = sct.grab(region)

        frame = np.array(img)
        frame = frame[:, :, :3]
        density = np.mean(frame)
        # print("density", density)
        return density <= 10

# buy_item(0,0)
# time.sleep(2)
# with mss.mss() as sct:
#     region = {"top": 1300, "left": 320, "width": 60, "height": 70}
#     img = sct.grab(region)
#
#     frame = np.array(img)
#     frame = frame[:, :, :3]
#     np.save(Path(__file__).resolve().parents[1] / "data" / "menu.npy", frame)