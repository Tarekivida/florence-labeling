# Florence-2 Image Labeling Tool

This is a simple CLI tool to automatically label images using [Microsoft's Florence-2](https://huggingface.co/microsoft/Florence-2-base) vision-language model.

It supports:
- ✅ Object detection
- 📝 Light image description
- 🧠 Extensive image captioning

All labels are exported to a CSV file (`labels.csv`) with full file paths and predictions.

---

## 🚀 How to Use

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/florence-labeling.git
cd florence-labeling
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the Script

```bash
python main.py /path/to/image/folder
```

The script will:
- Ask you to choose a labeling mode
- Recursively find all images in the folder and subfolders
- Label each image using Florence-2
- Save output in `labels.csv`

---

## 📦 CSV Output Format

| file_path            | file_name     | label                            |
|----------------------|---------------|----------------------------------|
| images/1.jpg         | 1.jpg         | A cat sitting on a couch         |
| images/road/photo.png | photo.png     | A street with several parked cars|

---

## 🔧 Labeling Options

At runtime, you’ll be prompted to choose:

1. **Object Detection** – Lists objects (e.g., "a dog, a ball")
2. **Light Description** – Simple caption (e.g., "A dog in a park")
3. **Extensive Description** – More detailed caption (e.g., "A brown dog playing fetch in a large green park")

---

## 📁 Folder Structure

```
florence-labeling/
├── main.py
├── requirements.txt
├── README.md
└── labels.csv  ← Generated after running the script
```

---

## ✅ Requirements

- Python ≥ 3.9
- Tested on macOS with Apple Silicon
- Florence-2 via Hugging Face (`microsoft/Florence-2-base`)

---

## 📄 License

MIT License — feel free to use, modify, and contribute.

---

## 🙏 Credits

Built with [Hugging Face Transformers](https://huggingface.co/docs/transformers), [Microsoft Florence-2](https://huggingface.co/microsoft/Florence-2-base), and ❤️ by [YOUR NAME].
