import os
import requests
import tkinter as tk
from tkinter import filedialog
from urllib.parse import urlparse

class ImageDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Downloader")
        
        # Default download path
        self.default_download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.download_path = tk.StringVar(value=self.default_download_path)
        
        # URL entry field
        tk.Label(root, text="Image URL:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Path entry field
        tk.Label(root, text="Download Path:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.path_entry = tk.Entry(root, textvariable=self.download_path, width=50)
        self.path_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.path_browse_button = tk.Button(root, text="Browse", command=self.browse_path)
        self.path_browse_button.grid(row=1, column=2, padx=10, pady=5)
        
        # Download button
        self.download_button = tk.Button(root, text="Download", command=self.download_image)
        self.download_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def browse_path(self):
        selected_path = filedialog.askdirectory()
        if selected_path:
            self.download_path.set(selected_path)

    def download_image(self):
        url = self.url_entry.get().strip()
        if not url:
            tk.messagebox.showerror("Error", "Please enter a valid image URL")
            return

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # Parse the URL to get the filename
            filename = os.path.basename(urlparse(url).path)
            download_path = os.path.join(self.download_path.get(), filename)

            # Download the image
            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            tk.messagebox.showinfo("Success", f"Image downloaded successfully to:\n{download_path}")

            # Reset URL entry
            self.url_entry.delete(0, tk.END)

        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to download image:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDownloaderApp(root)
    root.mainloop()
