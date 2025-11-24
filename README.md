# 🕷️ Website Scraper Pro

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

A powerful, intelligent website scraper with **search**, **analysis**, and **export** features. Perfect for collecting LLM training data, documentation scraping, and content analysis.

![Website Scraper Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=Website+Scraper+Pro)

## ✨ Features

### 🎯 Core Features
- **Full Website Scraping** - Automatically crawls and extracts complete content
- **Smart Search** - Find any word with yellow highlighting across all pages
- **Content Analysis** - Word count, reading time, and top 20 keywords
- **Multiple Exports** - JSON, TXT, and Markdown formats

### 🔍 Search & Highlight
- Real-time search across all scraped content
- Shows occurrence count per page
- **Yellow highlighting** of search terms
- Auto-scroll to first match

### 📊 Analysis Dashboard
- Total words and reading time
- Top keywords extraction
- Statistics per page
- Link and image analysis

### 📥 Export Options
- **JSON** - Structured data for processing
- **TXT** - Plain text corpus for LLM training
- **Markdown** - Clean, readable format

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/darshanmore2911/website-scraper-pro.git
cd website-scraper-pro

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Run the scraper
python run_scraper.py
```

**Input:**
```
📍 Enter website URL: example.com
📄 Max pages: 50
```

**Output:**
- Interactive HTML page opens in browser
- Markdown file generated
- All content ready for export

## 📸 Screenshots

### Interactive Dashboard
```
┌─────────────────────────────────────────┐
│  🕷️ Website Scraper                     │
│  example.com                             │
│  Developed by Darshan More               │
│                                          │
│  50 Pages | 20,316 Words | 101 Min Read │
└─────────────────────────────────────────┘
```

### Search with Highlighting
```
🔍 Search: "python"

Found 3 pages with "python"

Page 1: Python Documentation
5 occurrence(s)
[View & Highlight] ← Click to see highlighted results
```

### Export Options
```
📥 Export Options
┌──────────┬──────────┬──────────┐
│ JSON     │ TXT      │ Markdown │
└──────────┴──────────┴──────────┘
```

## 🎯 Use Cases

### 1. LLM Training Data
```bash
python run_scraper.py
# URL: docs.python.org
# Pages: 100
# Result: Clean text corpus ready for training
```

### 2. Documentation Backup
```bash
python run_scraper.py
# URL: your-docs-site.com
# Pages: 50
# Result: Complete documentation in multiple formats
```

### 3. Content Analysis
```bash
python run_scraper.py
# URL: competitor-blog.com
# Pages: 30
# Result: Keyword analysis and content insights
```

## 📁 Project Structure

```
website-scraper-pro/
├── run_scraper.py              # Main entry point
├── full_website_scraper.py     # Core scraping engine
├── content_analyzer.py         # Content analysis module
├── markdown_exporter.py        # Markdown export
├── simple_html_generator.py    # HTML generator with search
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── USAGE.md                    # Detailed usage guide
└── LICENSE                     # MIT License
```

## 🛠️ Technical Details

### Technologies Used
- **Python 3.8+**
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP requests
- **lxml** - Fast XML/HTML processing
- **tqdm** - Progress bars

### Key Features Implementation
- **Smart Crawling** - Follows internal links automatically
- **Polite Scraping** - 1-second delay between requests
- **Error Handling** - Robust retry logic
- **Memory Efficient** - Processes pages incrementally

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Speed** | ~1 page/second |
| **Memory** | ~50MB for 100 pages |
| **Accuracy** | 95%+ content extraction |
| **Formats** | 3 export formats |

## 🎓 Examples

### Example 1: Python Documentation
```python
# Scrapes Python docs and generates analysis
URL: docs.python.org
Pages: 100
Time: ~2 minutes
Output: 50,000+ words, 200+ keywords
```

### Example 2: Blog Content
```python
# Scrapes blog posts for content analysis
URL: techblog.com
Pages: 50
Time: ~1 minute
Output: Clean markdown, keyword insights
```

## 🔧 Configuration

### Customize Scraping
Edit `full_website_scraper.py`:
```python
# Change delay between requests
time.sleep(1)  # Default: 1 second

# Change max pages
max_pages = 50  # Default: 50
```

### Customize Analysis
Edit `content_analyzer.py`:
```python
# Change keyword count
stats['top_keywords'] = word_counts.most_common(20)  # Default: 20
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Ideas for Contributions
- [ ] Add support for JavaScript-heavy sites (Selenium)
- [ ] Implement database storage (SQLite)
- [ ] Add image downloading
- [ ] Create API endpoint
- [ ] Add scheduling/automation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Darshan More**

- 🌐 GitHub: [@darshanmore2911](https://github.com/darshanmore2911)
- 💼 LinkedIn: [in/darshanmore29](https://www.linkedin.com/in/darshanmore29)
- 📸 Instagram: [@itzdarshann](https://www.instagram.com/itzdarshann)
- 📍 Location: Nashik, India
- 🎓 CSE Undergrad | Python & Web Dev

*Passionate about clean code and real-world solutions.*

## ⭐ Show Your Support

If you find this project helpful, please give it a ⭐ on GitHub!

## 📧 Contact

Have questions or suggestions? Feel free to:
- Open an [issue](https://github.com/darshanmore2911/website-scraper-pro/issues)
- Connect on [LinkedIn](https://www.linkedin.com/in/darshanmore29)
- Follow on [Instagram](https://www.instagram.com/itzdarshann)

## 🙏 Acknowledgments

- Built with Python and love ❤️
- Inspired by the need for clean LLM training data
- Thanks to the open-source community

---

**Made with ❤️ by [Darshan More](https://github.com/darshanmore2911)**

© 2025 Darshan More. All rights reserved.
