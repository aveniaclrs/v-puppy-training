import tkinter as tk
from tkinter import scrolledtext, font 
from openai import OpenAI

# Set your OpenAI API key (Assume you have it already)
client = OpenAI(
    # This is the default and can be omitted
    api_key="",
)

# Create the main window
root = tk.Tk()
root.title("DogBot - Ask Me Anything")
root.geometry("500x500")

# Fonts
user_font = font.Font(family="Helvetica", size=14, weight="bold")
bot_font = font.Font(family="Helvetica", size=14)
input_font = font.Font(family="Arial", size=14)

# Configure grid weights to make layout responsive
root.grid_rowconfigure(0, weight=1)  # Chat history expands vertically
root.grid_columnconfigure(0, weight=1)  # Chat history expands horizontally
def generate_openai_response(question):
    """Generate a friendly, concise response personalized for Ave and their Poochon."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are DogBot, an intelligent assistant designed to help new dog parents take care of their dogs. "
                    "The user is named 'Ave, 🐾' and they have a Poochon (a mix of Poodle and Bichon Frise). "
                    "Provide step-by-step guidance on essential tasks such as feeding, training, socializing, grooming, and health care. "
                    "Tailor your advice to the specific needs of a Poochon, including its grooming requirements, temperament, and common health issues. "
                    "Offer practical tips, explain challenges, and suggest friendly solutions that Ave can easily follow to keep their Poochon happy and healthy."
                )},
                {"role": "user", "content": question}
            ],
            max_tokens=500
        )
        answer = response.choices[0].message.content.strip()
        return answer  # No extra greeting here
    except Exception as e:
        return f"Error: {str(e)}"

def send_message(event=None):
    """Handles sending messages."""
    question = user_input.get()
    if question.strip():
        chat_history.insert(tk.END, f"You: {question}\n")
        user_input.delete(0, tk.END)

        response = generate_openai_response(question)
        chat_history.insert(tk.END, f"Bot: {response}\n\n")  # Add greeting only here
        chat_history.see(tk.END)

# Chat History Text Area
chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='normal', font=bot_font)
chat_history.tag_config("user", foreground="blue", font=user_font)
chat_history.tag_config("bot", foreground="green", font=bot_font)
chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# User Input Field
user_input = tk.Entry(root, font=input_font)
user_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Send Button
send_button = tk.Button(root, text="Send", command=send_message, font=input_font)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Bind Enter key to send_message function
user_input.bind("<Return>", send_message)

# Make the input field expand with window resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Run the GUI event loop
root.mainloop()