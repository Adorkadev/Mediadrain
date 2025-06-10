import filetype
from videoprops import get_video_properties
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Label, Button, RAISED
from windows_monitors import monitor_areas
import random as rand

MIN_SCALE = 0.2
MAX_SCALE = 0.5

def kill():
    os.kill(os.getpid(), 9)

def run(path):
    # get media type and format
    kind = filetype.guess(path)
    if kind is None:
        print('Cannot guess file type!')
        return False
    type = str.split(kind.mime, "/")[0]
    fmt = str.split(kind.mime, "/")[1]
    print('File: %s' % path)
    print('File type: %s' % type)
    print('File format: %s' % fmt)

    # load in media
    if (type == "image"):
        image = Image.open(path)
    elif (type == "video"):
        video_properties = get_video_properties(path)
        image = Image.new('RGB', (video_properties['width'], video_properties['height']))
    else:
        return False

    # choose random monitor
    monitors = monitor_areas()
    monitor_data = list(monitors[rand.randrange(0, len(monitors))][2])
    print(monitor_data)
    monitor_width = monitor_data[2] - monitor_data[0]
    monitor_height = monitor_data[3] - monitor_data[1]

    # choose scale (% of monitor size)
    target_scale = rand.random() * (MAX_SCALE-MIN_SCALE) + MIN_SCALE

    # resize image
    source_scale = max(image.width, image.height) / min(monitor_width, monitor_height)
    resize_factor = target_scale / source_scale
    image = image.resize((round(image.width*resize_factor), round(image.height*resize_factor)), Image.LANCZOS)

    # tkinter window
    root = Tk()
    root.configure(bg='black')
    root.overrideredirect(1)
    root.frame = Frame(root)
    root.wm_attributes('-topmost', 1)

    # convert to tkinter image
    tk_image = ImageTk.PhotoImage(image)

    if (type == "video"):
        # todo: implement
        return False
    elif (fmt == "gif"):
        # todo: implement
        return False
    else:
        label = Label(root, image=tk_image, bg='black')
        label.pack()

    # choose random position on monitor
    posX = rand.randint(monitor_data[0], max((monitor_data[2] - image.width), monitor_data[0]))
    posY = rand.randint(monitor_data[1], max((monitor_data[3] - image.height), monitor_data[1]))

    # set window geometry
    root.geometry(f'{image.width}x{image.height}+{posX}+{posY}')
    print(f'{image.width}x{image.height}+{posX}+{posY}')

    # add button to close window
    close_button = Button(root, text="Gone Forever~", command=kill)
    close_button.place(x=image.width - 5 - close_button.winfo_reqwidth(), y=image.height - 5 - close_button.winfo_reqheight())

    # # start tkinter window
    image.close()
    root.mainloop()
    return True

if __name__ == '__main__':
    import os
    import random

    def select_random_file(directory):
        """Select a random file from the given directory."""
        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            if not files:
                raise FileNotFoundError("No files found in the directory.")
            return os.path.join(directory, random.choice(files))
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
    
    while (not run(select_random_file("D:\Projects\Adorkabot\spankbank"))):
        pass