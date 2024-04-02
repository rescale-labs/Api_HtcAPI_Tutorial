import sys
import cv2
import time
import os
import boto3
import random
import subprocess
from pathlib import Path


def face_detect(
    image_path,
    cascasde_path="/usr/local/lib/python3.10/site-packages/cv2/data/haarcascade_frontalface_default.xml",
):
    start = time.time()
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cascasde_path)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + h, y + h), (0, 255, 0), 2)

    img_file_path = f"{image_path}_tagged.jpg"
    dat_file_path = f"{image_path}_tagged.dat"

    if len(faces) > 0:
        cv2.imwrite(img_file_path, image)
        with open(dat_file_path, "w") as f:
            f.write(f"face_cnt\n{len(faces)}")

    print(f"{image_path}: Found {len(faces)} faces in {time.time()-start} seconds.")

    return len(faces), img_file_path, dat_file_path


def _call_htcctl(cmd, project_shared):
    if project_shared: cmd.insert(1, "-s")

    p = subprocess.run(cmd)
    print([p.stdout, p.stderr], sep="\n")
    if p.returncode != 0:
        sys.exit(os.EX_IOERR)


def upload_files(file_paths_list, project_shared=False):
    cmd = ["htcctl", "upload"] + file_paths_list
    _call_htcctl(cmd, project_shared)


def download_files(object_keys_list, project_shared=False):
    cmd = ["htcctl", "download"] + object_keys_list
    _call_htcctl(cmd, project_shared)


def htc_detect(input_image):
    # Download from project storage
    download_files([input_image], project_shared=True)

    face_cnt, img_file_path, dat_file_path = face_detect(input_image)

    if face_cnt > 0:
        # Upload to task storage
        upload_files([img_file_path, dat_file_path])


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def htc_batch_detect(img_objkey_list, batch_index, batch_size, sim_fail):
    download_files([img_objkey_list], project_shared=True)

    with open(img_objkey_list, "r") as f:
        image_names = [l.strip() for l in f.readlines()]
    chunks = list(_chunks(image_names, int(len(image_names) / batch_size)))

    # This is used to simulate failures
    if sim_fail and random.randint(0, 2) == 1:
        if random.randint(0, 2) == 1:
            raise Exception("Simulated exception")
        else:
            # spin for 1h to simulate execTimeout
            time.sleep(3600)

    for img_file in chunks[batch_index]:
        htc_detect(img_file)


if __name__ == "__main__":
    if "SHOW_ENV" in os.environ:
        for name, value in os.environ.items():
            print("{0}: {1}".format(name, value))

    if "HTC_INPUT_IMAGE" in os.environ:
        htc_detect(sys.argv[1])
    elif len(sys.argv) == 1:
        img_objkey_list = os.environ["IMG_OBJKEY_LIST"]
        batch_index = int(os.environ["AWS_BATCH_JOB_ARRAY_INDEX"])
        batch_size = int(os.environ["BATCH_JOB_ARRAY_SIZE"])
        sim_fail = "SIMULATE_FAILURES" in os.environ
        htc_batch_detect(
            img_objkey_list, batch_index, batch_size, sim_fail
        )
    else:
        face_detect(sys.argv[1])
