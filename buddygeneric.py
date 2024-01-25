import os
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import json


#Goes through the frames of the current gif that should be played
class ImagePlayer:
    def __init__(self, image_path, label, delay = 100):
        self.delay = delay
        self.label = label
        # Open the animated image file
        self.image = Image.open(image_path)
        self.image_path = image_path

        # Extract all frames from the animated image
        self.frames = [frame.copy() for frame in ImageSequence.all_frames(self.image)]
        self.num_frames = len(self.frames)

        # Set the initial frame
        self.current_frame = 0

    def update_image(self):
        # Get the next frame
        over = False
        if (self.current_frame >= self.num_frames-1):
            self.current_frame = 0
            over = True
            
        else:
            self.current_frame += 1
        frame = self.frames[self.current_frame]
        # Move to the next frame
        return ImageTk.PhotoImage(frame), over

#Single State
class State:
    def __init__(self, name, next_states, image_path, label, delay, x_transform, y_transform):
        self.name = name
        self.next_states = next_states
        self.image_file = image_path
        self.image_player = ImagePlayer(image_path, label, delay)
        self.x_transform = x_transform
        self.y_transform = y_transform

    def get_next_states(self):
        return self.next_states
    
    def get_image_path(self):
        return get_path(self.image_file)

    def get_image_player(self):
        return self.image_player

#Goes through the states of the gif
class StateManager:
    def __init__(self, states, x, y):
        self.states = states
        self.current_state_index = 0
        self.x = x
        self.y = y

    def get_current_state(self):
        return self.states[self.current_state_index]

    def get_next_state_options(self):
        current_state = self.get_current_state()
        return current_state.get_next_states()

    def random_transition(self):
        next_state_options = self.get_next_state_options()
        if next_state_options:
            self.current_state_index = random.choice(next_state_options)
        
#load states
def play_next_frame(current_state, label):
    print("Current State:", state_manager.get_current_state().name)
    current_player = current_state.get_image_player()
    photo,over = current_player.update_image()
    if over:
        root.after(1, play_random_image_player, label)
        return
    current_player.label.config(image=photo)
    current_player.label.image = photo
    state_manager.x = SCREEN_WIDTH if state_manager.x + current_state.x_transform > SCREEN_WIDTH else 0 if state_manager.x + current_state.x_transform < 0 else state_manager.x + current_state.x_transform
    state_manager.y = SCREEN_HEIGHT if state_manager.y + current_state.y_transform > SCREEN_HEIGHT else 0 if state_manager.y + current_state.y_transform < 0 else state_manager.y + current_state.y_transform
    root.geometry('100x100+' + str(state_manager.x) + '+' + str(state_manager.y))
    root.after(current_player.delay, play_next_frame, current_state, label)

#load states
def play_first_image(label):
    # Play the current player
    current_state = state_manager.get_current_state()
    root.after(1, play_next_frame, current_state, label)

#load states
def play_random_image_player(label):
    # Get the next state and update the StateManager
    state_manager.random_transition()
    current_state = state_manager.get_current_state()
    # Schedule the next player to play
    root.after(1, play_next_frame, current_state, label)

def load_states_from_json(json_file, label, x_coordinate=0, y_coordinate=0):
    with open(json_file, 'r') as file:
        data = json.load(file)

    states = []
    for state_data in data['states']:
        state = State(state_data['name'], state_data['next_states'], get_path(state_data['image_file']), label, state_data['delay'],state_data['x_transform'], state_data['y_transform'])
        states.append(state)

    return StateManager(states, x_coordinate, y_coordinate)

def get_path(filename):
    # Get the full path from the filename using the current working directory
    return os.path.join(os.getcwd(), 'Assets\\', filename) #.replace('\\', '/')


json_file_path = 'states.json'

# Set up the Tkinter window
root = tk.Tk()
root.title("Animated Image Players")

#Adjust location
x_coordinate = (root.winfo_screenwidth() -100) // 2
y_coordinate = (root.winfo_screenheight()- 200) //1
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

# Window configuration
root.config(highlightbackground='black')
label = tk.Label(root, bd=0, bg='black')
root.overrideredirect(True)
root.wm_attributes('-transparentcolor', 'black')
root.wm_attributes('-topmost', 1)  # Make the window stay on top
# Create a single label to display the images
label.pack()

# Create an instance of StateManager with the list of states
state_manager = load_states_from_json(json_file_path, label, x_coordinate, y_coordinate)

# Start playing first image
root.after(1,play_first_image,label)

# Run the Tkinter main loop
root.mainloop()
