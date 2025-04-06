# 📦 GitHub Repo to JSON Converter

A simple Python script that clones a public GitHub repository, recursively scans all files, and saves their content in a structured JSON format.

## 🧰 Features

- Clones any **public GitHub repository**  
- Recursively collects all **non-hidden files**  
- Stores:
  - `filename`
  - `relative path`
  - `full file content` as a string  
- Outputs a single `repo_contents.json` file  
- Automatically deletes temporary files after execution  
- Logs all actions and warnings  

## 🖥️ Requirements

- Python **3.7+**
- `gitpython` library

Install dependencies:

```bash
pip install gitpython
```

## 🚀 Usage

Clone this project or copy `main.py`:

```bash
git clone https://github.com/your-username/converting-repo-to-json.git
cd converting-repo-to-json
```

Run the script:

```bash
python main.py
```

Enter the URL of a **public GitHub repository** when prompted.

The script will generate `repo_contents.json` in the current directory.

## 📝 JSON Format

The output file (`repo_contents.json`) will look like this:

```json
[
  {
    "filename": "example.py",
    "path": "src/example.py",
    "content": "print('Hello, world!')"
  }
]
```

## 🧹 Notes

- Hidden files and directories (like `.git`) are ignored  
- Binary or unreadable files are skipped (their content will be an empty string)  
- Temporary files are automatically cleaned up after execution  

## 📄 License

MIT License
