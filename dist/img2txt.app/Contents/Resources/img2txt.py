import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pytesseract
import csv

# Set up pytesseract to use the appropriate tesseract executable path
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def extract_text_from_images():
    global extracted_texts
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        try:
            extracted_texts = []
            for file_path in file_paths:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                extracted_texts.append({'File': file_path, 'Text': text})
                display_text.insert(tk.END, f"Text extracted from: {file_path}\n")
                display_text.insert(tk.END, text + '\n\n')
            show_notification("Text extraction completed.")
        except Exception as e:
            show_notification(f"Error extracting text: {str(e)}")

def export_to_csv():
    if extracted_texts:
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['File', 'Text']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for extracted_text in extracted_texts:
                        writer.writerow(extracted_text)
                show_notification("Export to CSV completed.")
        except Exception as e:
            show_notification(f"Error exporting to CSV: {str(e)}")

def show_notification(message):
    notification_label.config(text=message)
    root.after(3000, clear_notification)

def clear_notification():
    notification_label.config(text="")

# GUI setup
root = tk.Tk()
root.title("Img2Txt - Image to Text Converter")

extracted_texts = []

main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=20)

tk.Label(main_frame, text="Select image files:").pack()

button_frame = tk.Frame(main_frame)
button_frame.pack()

select_button = tk.Button(button_frame, text="Select Images", command=extract_text_from_images)
select_button.pack(padx=10, pady=10)

export_button = tk.Button(button_frame, text="Export to CSV", command=export_to_csv)
export_button.pack(padx=10, pady=10)

display_text = tk.Text(main_frame, height=15, width=80)
display_text.pack(pady=20)

notification_label = tk.Label(root, text="", fg="red")
notification_label.pack()

root.mainloop()
