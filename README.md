# GitHub Issue-based Troubleshooting Guide Generator

This project generates a **Troubleshooting Guide in Markdown format** by analyzing **closed issues** from a specified GitHub repository. It uses the OpenAI API to summarize and classify each issue into a structured format: **Problem / Cause / Solution**.

## 🚀 Features

- Automatically extracts closed issues from any GitHub repository
- Summarizes issues using OpenAI API
- Outputs a clean and structured Markdown troubleshooting guide

---

## 🧰 Requirements

- **OpenAI API Key**
- **GitHub Personal Access Token (PAT)**

---

## 🔑 OpenAI API Key

Insert your OpenAI API key in the script like this:

```python
client = openai.OpenAI(api_key="your-key-here")
```

## ⚙️ How to Run

```terminal
python3 ./TSG_maker.py <GitHub_TOKEN> <OWNER> <REPO> --output <OUTPUT_FILENAME>
```


### 🔧 Parameters

| Argument      | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `TSG_maker.py`| Python script to run                                                        |
| `ghp_...`     | Your GitHub Personal Access Token                                           |
| `OWNER`       | GitHub username or organization name (e.g., `WIZnet-ioNIC`)                 |
| `REPO`        | Repository name (e.g., `WIZnet-PICO-C`)                                     |
| `--output`    | Optional argument to specify the name of the output Markdown file (e.g., `WIZnet_PICO_Troubleshooting.md`) |

