import openai
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def interpret_title(title):
    print("Interpreting title...")
    print(title)
    try:
        # Create a list of messages for chat completion
        messages = [
            {"role": "system", "content": "Create a visual pun or a playful, abstract representation based on the words in the title."},
            {"role": "user", "content": title}
        ]
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Adjust the model as per your subscription plan
            messages=messages,
            max_tokens=60
        )
        interpretation = response.choices[0].message.content.strip()
        print("Interpreted:", interpretation)
        return interpretation
    except Exception as e:
        print(f"Error during interpretation: {e}")
        return None


def generate_image(title_interpretation):
    print("Generating image...")
    try:
        response = openai.images.generate(
            model="dall-e-2",
            prompt=title_interpretation,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        print("Image URL:", image_url)
        return image_url
    except Exception as e:
        print(f"Error during image generation: {e}")
        return None

def load_image_from_url(url):
    print("Loading image from URL...")
    try:
        response = requests.get(url)
        image_data = response.content
        return Image.open(BytesIO(image_data))
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def refresh_image(canvas, image_url):
    print("Refreshing image on canvas...")
    image = load_image_from_url(image_url)
    if image:
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(20, 20, anchor='nw', image=photo)
        canvas.image = photo
        print("Image displayed.")
    else:
        print("Failed to load or display image.")

def setup_gui():
    print("Setting up GUI...")
    root = tk.Tk()
    root.geometry('1024x1080')  # Increase the window size to accommodate all elements

    # Use a frame to better organize the canvas and other widgets
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame, width=1024, height=1024, bg='white')
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    entry = tk.Entry(frame, bg='white', fg='black')
    # entry.pack(side=tk.TOP, padx=20, pady=20)  # Add padding to ensure it's not obscured by the canvas
    entry.place(x=200, y=20)

    # Define a reasonably-sized button
    button = tk.Button(frame, width=10, height=10, text='Generate', bg='black', fg='white', command=lambda: generate_and_refresh_image(canvas, entry.get()))
    # button.pack(side=tk.TOP, pady=10)  # Add some padding and place it below the entry widget
    button.place(x=65, y=10)

    print("GUI ready. Waiting for user input...")
    root.mainloop()

def generate_and_refresh_image(canvas, title):
    print("Processing title:", title)
    title_interpretation = interpret_title(title)
    if title_interpretation:
        image_url = generate_image(title_interpretation)
        if image_url:
            refresh_image(canvas, image_url)
        else:
            print("Image URL generation failed.")
    else:
        print("Title interpretation failed.")

if __name__ == '__main__':
    setup_gui()
