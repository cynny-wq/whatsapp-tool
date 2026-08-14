import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import urllib.parse


def generate_links():
    # 1. Get the custom message from the text box
    message_template = message_entry.get("1.0", tk.END).strip()

    if not message_template:
        messagebox.showerror("Error", "Please type a message template first.")
        return

    # 2. Ask the user to select the input CSV file
    input_file = filedialog.askopenfilename(
        title="Select Customer CSV File", filetypes=[("CSV Files", "*.csv")]
    )
    if not input_file:
        return

    # 3. Ask the user where to save the finished file
    output_file = filedialog.asksaveasfilename(
        title="Save WhatsApp Links As",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
    )
    if not output_file:
        return

    try:
        with open(
            input_file, mode="r", encoding="utf-8"
        ) as infile, open(
            output_file, mode="w", newline="", encoding="utf-8"
        ) as outfile:
            reader = csv.DictReader(infile)

            if "Name" not in reader.fieldnames or (
                "Phone" not in reader.fieldnames
            ):
                messagebox.showerror(
                    "Error", "CSV must contain 'Name' and 'Phone' columns."
                )
                return

            writer = csv.writer(outfile)
            writer.writerow(["Name", "Phone", "WhatsApp Link"])

            for row in reader:
                name = row["Name"]
                phone = row["Phone"].replace(" ", "").replace("+", "")

                # Safely replace {name} placeholder if it exists
                custom_message = message_template.replace("{name}", name)
                encoded_message = urllib.parse.quote(custom_message)
                whatsapp_url = f"https://wa.me{phone}?text={encoded_message}"

                writer.writerow([name, phone, whatsapp_url])

        messagebox.showinfo("Success", "Finished! Your file is ready to use.")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {str(e)}")


# --- Build the User Interface Window ---
root = tk.Tk()
root.title("WhatsApp Link Tools")
root.geometry("450x350")

# App Header
title_label = tk.Label(
    root, text="WhatsApp Tool", font=("Arial", 16, "bold"), fg="#25D366"
)
title_label.pack(pady=10)

# Input Box Label
msg_label = tk.Label(
    root,
    text="Type your message below. Use {name} where the customer's name should go:",
    font=("Arial", 9, "italic"),
)
msg_label.pack(pady=5)

# Text Box for Custom Message
message_entry = tk.Text(root, height=5, width=45, font=("Arial", 10))
message_entry.pack(pady=5)
# Insert a default message so it's not empty
message_entry.insert(
    "1.0",
    "Hello {name}, thank you for shopping with us! Your order is ready for pickup.",
)

# The Main Action Button
start_button = tk.Button(
    root,
    text="Upload CSV & Generate Links",
    command=generate_links,
    font=("Arial", 11, "bold"),
    bg="#25D366",
    fg="black",
    padx=10,
    pady=8,
)
start_button.pack(pady=20)

root.mainloop()
