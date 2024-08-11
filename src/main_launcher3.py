import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from collections import Counter
import nltk
from nltk.tokenize import RegexpTokenizer
import os
import PyPDF2

nltk.download('punkt')

# Define whitelist file path (configurable)
WHITELIST_FILE = "whitelist.txt"

class WordFrequencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Frequency Analyzer")

        # Adjust window size and position
        self.root.geometry("800x600")
        self.center_window()

        # Font settings
        font = ("Arial", 12)

        # File selection button
        self.select_button = tk.Button(root, text="Select PDF File", command=self.select_file, font=font, bg="#f0f0f0")
        self.select_button.pack(pady=15)

        # Analyze button
        self.analyze_button = tk.Button(root, text="Analyze Word Frequency", command=self.analyze, font=font, bg="#f0f0f0")
        self.analyze_button.pack(pady=15)

        # Manage whitelist button
        self.manage_whitelist_button = tk.Button(root, text="Manage Whitelist", command=self.manage_whitelist, font=font, bg="#f0f0f0")
        self.manage_whitelist_button.pack(pady=15)

        # Show whitelist button
        self.show_whitelist_button = tk.Button(root, text="Show Whitelist", command=self.show_whitelist, font=font, bg="#f0f0f0")
        self.show_whitelist_button.pack(pady=15)

        # Status label
        self.status_label = tk.Label(root, text="", font=font, anchor="w")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=5)

        # Result display area
        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Create a treeview for displaying results
        self.result_tree = ttk.Treeview(self.result_frame, columns=("word", "frequency"), show="headings")
        self.result_tree.heading("word", text="Word")
        self.result_tree.heading("frequency", text="Frequency")
        self.result_tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.selected_file = None
        self.word_freq = None  # To store word frequency for whitelist management
        self.word_list = []    # To store words in order for management and display

    def center_window(self):
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - 600 / 2)
        position_right = int(screen_width / 2 - 800 / 2)
        self.root.geometry(f"800x600+{position_right}+{position_top}")

    def select_file(self):
        filetypes = (("PDF files", "*.pdf"), ("All files", "*.*"))
        self.selected_file = filedialog.askopenfilename(title="Open a file", filetypes=filetypes)
        if self.selected_file:
            self.status_label.config(text=f"Selected file: {os.path.basename(self.selected_file)}")

    def analyze(self):
        if not self.selected_file:
            messagebox.showwarning("No File Selected", "Please select a PDF file first.")
            return

        text = self.extract_text_from_pdf(self.selected_file)
        if not text:
            messagebox.showerror("Error", "Failed to extract text from PDF file.")
            return

        # Load whitelist
        whitelist = self.load_whitelist()

        # Tokenization and frequency analysis
        tokenizer = RegexpTokenizer(r'\b[a-zA-Z]+\b')  # Only retain word characters (letters only)
        words = tokenizer.tokenize(text.lower())
        self.word_freq = Counter(word for word in words if word not in whitelist)
        self.word_list = [word for word, _ in self.word_freq.most_common()]  # Order for display

        # Display results
        self.result_tree.delete(*self.result_tree.get_children())
        for word, freq in self.word_freq.most_common():
            self.result_tree.insert("", tk.END, values=(word, freq))

        self.status_label.config(text="Analysis complete!")

    def extract_text_from_pdf(self, pdf_file):
        text = ""
        try:
            with open(pdf_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"Error extracting text: {e}")
            return None
        return text

    def load_whitelist(self):
        if not os.path.exists(WHITELIST_FILE):
            return set()
        with open(WHITELIST_FILE, 'r') as file:
            return set(file.read().splitlines())

    def save_whitelist(self, whitelist):
        with open(WHITELIST_FILE, 'w') as file:
            file.write("\n".join(sorted(whitelist)))

    def manage_whitelist(self):
        if self.word_freq is None:
            messagebox.showwarning("No Analysis", "Please run the analysis first.")
            return

        whitelist = self.load_whitelist()
        whitelist_window = tk.Toplevel(self.root)
        whitelist_window.title("Manage Whitelist")
        whitelist_window.geometry("600x400")
        self.center_window_in_parent(whitelist_window, 600, 400)

        label = tk.Label(whitelist_window, text="Select words to add to whitelist:", font=("Arial", 12))
        label.pack(pady=10)

        listbox = tk.Listbox(whitelist_window, selectmode=tk.MULTIPLE, font=("Arial", 10))
        for word in self.word_list:
            if word.strip():
                listbox.insert(tk.END, word)
        listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        add_button = tk.Button(whitelist_window, text="Add to Whitelist", command=lambda: self.add_to_whitelist(listbox, whitelist_window), font=("Arial", 12), bg="#f0f0f0")
        add_button.pack(pady=10)

    def add_to_whitelist(self, listbox, whitelist_window):
        selected_words = [listbox.get(i).strip() for i in listbox.curselection()]
        whitelist = self.load_whitelist()
        for word in selected_words:
            if word and word not in whitelist:
                whitelist.add(word)
        self.save_whitelist(whitelist)
        whitelist_window.destroy()
        self.analyze()  # Refresh the word frequency results

    def show_whitelist(self):
        whitelist = self.load_whitelist()
        whitelist_window = tk.Toplevel(self.root)
        whitelist_window.title("Show Whitelist")
        whitelist_window.geometry("400x400")
        self.center_window_in_parent(whitelist_window, 400, 400)

        label = tk.Label(whitelist_window, text="Current Whitelist:", font=("Arial", 12))
        label.pack(pady=10)

        listbox = tk.Listbox(whitelist_window, font=("Arial", 10))
        for word in self.word_list:
            if word in whitelist:
                listbox.insert(tk.END, word)
        listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        close_button = tk.Button(whitelist_window, text="Close", command=whitelist_window.destroy, font=("Arial", 12), bg="#f0f0f0")
        close_button.pack(pady=10)

    def center_window_in_parent(self, window, width, height):
        parent_x = self.root.winfo_x()
        parent_y = self.root.winfo_y()
        parent_width = self.root.winfo_width()
        parent_height = self.root.winfo_height()
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WordFrequencyApp(root)
    root.mainloop()
