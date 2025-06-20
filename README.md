# 🧠 Semantic Job Application Auto Fill

This project automates filling out online job applications using **Selenium**, **TensorFlow Universal Sentence Encoder**, and **semantic similarity** to match form labels with field values.

It works especially well on **Greenhouse**, **AshbyHQ**, and similar applicant tracking systems (ATS) that follow accessible HTML labeling.

---

## 🔍 Features

- ✅ Semantic matching between config keys (like "first name") and website labels
- ✅ Fills both text fields and dropdowns
- ✅ Supports iframe-based forms (e.g., Greenhouse)
- ✅ Supports uploading resume and cover letter
- ✅ YAML-based configuration for easy reuse
- ✅ Works with Docker for isolation

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Selenium** – for browser automation
- **TensorFlow Hub** – Universal Sentence Encoder
- **ChromeDriver**
- **Docker (optional)** – for containerized execution

---

## 📦 Installation

### 🔹 Local Setup

1. **Clone the repo**:
   ```bash
   git clone https://github.com/yourusername/semantic-job-filler.git
   cd semantic-job-filler
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver**:  
   Make sure it matches your Chrome version: https://chromedriver.chromium.org/downloads

---

### 🔹 Docker Setup (Optional)

```bash
docker build -t semantic-job-filler .
docker run -v $(pwd):/app -it --rm semantic-job-filler
```

> Make sure Docker has access to the host display if you want GUI access. Or use headless mode.

---

## 📋 Configuration

Edit the `config.yaml` file with your details:

```yaml
url: "https://jobs.example.com/..."
first_name: "John"
last_name: "Doe"
email: "john@example.com"
...
```

Make sure `resume_path` and `cover_letter_path` are absolute paths to local PDF files.

---

## ⚙️ Usage

```bash
python main.py
```

It will:

- Launch Chrome
- Load the job application URL
- Use semantic matching to find and fill inputs
- Upload resume and cover letter
- Leave the final step to human verification and submit

---

## 🧠 How It Works

- It loads all visible `<label>` elements on the form
- Embeds each label using the **Universal Sentence Encoder**
- Matches your `config.yaml` keys with the closest label using **cosine similarity**
- Fills the value into the corresponding field

---

## 🛑 Notes & Limitations

- Not all ATS systems follow semantic labeling; results may vary
- This does **not** auto-submit to avoid misfires
- CAPTCHA or multi-step forms are not yet supported

---

## 🧑‍💻 Author

**Karthik Chandran Lakshmanasamy**  
[LinkedIn](https://linkedin.com/in/karthik-chandran-lakshmanasamy-a7232094)

---

## 📄 License

MIT License – use, fork, and share freely.
