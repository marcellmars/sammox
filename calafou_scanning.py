import subprocess, os

devices = [x for x in subprocess.check_output(["gphoto2", "--auto-detect"]).split() if "usb" in x]

def capture_photos(left, right, directory):
    for n, device in enumerate(devices):
        print n
        filename = left
        if n == 1:
            filename = right
        subprocess.call(["gphoto2", "--port", device, "--set-config", "capturetarget=card"])
        subprocess.call(["gphoto2", "--port", device, "--capture-image-and-download"])
        os.rename("capt0000.jpg", "{}".format(filename))
