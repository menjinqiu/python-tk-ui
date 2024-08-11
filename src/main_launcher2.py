import tkinter as tk
from tkinter import Menu, Button, filedialog, scrolledtext, ttk, messagebox, Listbox
from PyPDF2 import PdfReader
import re
from collections import Counter
from pathlib import Path



class WordFrequencyAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Frequency Analyzer-单词分析")
        self.ignored_words = self.load_ignored_words()


        # 创建菜单栏
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open PDF", command=self.open_pdf)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_app)
        ignore_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ignore", menu=ignore_menu)
        ignore_menu.add_command(label="Select Words to Ignore", command=self.show_word_list)

        # 创建Notebook控件
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # 创建第一个标签页，用于显示PDF文本
        self.text_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.text_tab, text='Text')

        # 创建文本显示区域用于PDF内容
        self.pdfTextArea = scrolledtext.ScrolledText(self.root, width=80, height=15)
        self.pdfTextArea.pack(side='top', fill='both', expand=True)

        # 创建文本显示区域用于词频结果
        self.wordFreqTextArea = scrolledtext.ScrolledText(self.root, width=80, height=15)
        self.wordFreqTextArea.pack(side='top', fill='both', expand=True)


        # 创建第二个标签页，用于显示词频分析结果
        self.analysis_tab = ttk.Frame(self.notebook)
        self.analysisText = scrolledtext.ScrolledText(self.analysis_tab, width=80, height=15)
        self.analysisText.pack(side='left', fill='both', expand=True)
        self.notebook.add(self.analysis_tab, text='Analysis')

        # 创建状态栏
        self.statusBar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor='w')
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)



    def load_ignored_words(self):
        ignored_words_path = Path("ignored_words.txt")
        ignored_words = set()
        if ignored_words_path.exists():
            with open(ignored_words_path, 'r') as file:
                ignored_words = {line.strip().lower() for line in file.readlines()}  # 使用 set 推导式
        return ignored_words




    def save_ignored_words(self, words):
        with open("ignored_words.txt", 'a') as file:
            for word in words:
                if word not in self.ignored_words:
                    file.write(word + '\n')
                    self.ignored_words.add(word)

    def show_word_list(self):
        top = tk.Toplevel(self.root)
        top.title("Select Words to Ignore")

        # 创建搜索框
        search_entry = tk.Entry(top)
        search_entry.pack(side='top', fill='x')

        # 创建单词列表
        self.word_listbox = tk.Listbox(top, width=80, height=15, selectmode='multiple')
        self.word_listbox.pack(side='left', fill='both', expand=True)

        # 填充单词列表
        self.update_word_list(self.sorted_word_counts)

        # 定义搜索功能
        def search_words(event):
            search_query = search_entry.get().lower()
            self.word_listbox.delete(0, tk.END)
            for word, count in self.sorted_word_counts:
                if search_query in word:
                    self.word_listbox.insert(tk.END, word)

        search_entry.bind("KeyRelease", search_words)

        # 添加确认按钮
        confirm_button = Button(top, text="Confirm Ignore", command=self.confirm_ignore_words)
        confirm_button.pack(side='bottom')

    def update_word_list(self, word_counts):
        for word, count in word_counts:
            self.word_listbox.insert(tk.END, f"{word}: {count}")

    def get_unique_words(self):
        text = self.pdfTextArea.get('1.0', tk.END).lower()  # 从PDF文本区域获取文本
        text = re.sub(r'[^a-z\s]', '', text)  # 清洗文本
        words = text.split()  # 分词
        return Counter(words)  # 计算词频

    def confirm_ignore_words(self):
        selected_indices = self.word_listbox.curselection()
        selected_words = [self.word_listbox.get(i).split(': ')[0] for i in selected_indices]
        self.save_ignored_words(selected_words)
        messagebox.showinfo("Success", "Selected words have been added to the ignore list.")
        self.show_word_frequencies()

    def show_word_frequencies(self):
        word_counts = self.get_unique_words()
        # Filter and sort by word frequency
        self.sorted_word_counts = sorted(
            ((word, count) for word, count in word_counts.items() if word not in self.ignored_words),
            key=lambda item: item[1],
            reverse=True
        )
        self.display_word_frequencies()

    def display_word_frequencies(self):
        self.analysisText.delete('1.0', tk.END)
        for word, count in self.sorted_word_counts:
            self.analysisText.insert(tk.END, f"{word}: {count}\n")

    def open_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filepath:
            self.load_pdf(filepath)

    def load_pdf(self, filepath):
        try:
            with open(filepath, 'rb') as file:
                reader = PdfReader(file)
                content = "\n".join(page.extract_text() for page in reader.pages)
            self.pdfTextArea.delete('1.0', tk.END)
            self.pdfTextArea.insert('1.0', content)
            self.statusBar.config(text="PDF loaded successfully")
        except Exception as e:
            self.statusBar.config(text="Error loading PDF")
            print(e)

    def exit_app(self):
        self.root.destroy()





def start_with_ui2():
    root = tk.Tk()
    app = WordFrequencyAnalyzer(root)
    Button(app.text_tab, text="Analyze Word Frequency", command=app.show_word_frequencies).pack(side='bottom')
    root.mainloop()

