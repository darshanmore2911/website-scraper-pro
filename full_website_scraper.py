"""
Complete Website Content Scraper for LLM Training

Features:
- URL do → Full website scrape ho jayega
- Har page ka complete content extract hoga
- Automatically browser me beautiful format me open hoga
- LLM training ke liye ready

Usage:
    py full_website_scraper.py
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import re
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import webbrowser
import time


class FullWebsiteScraper:
    """Complete website content scraper."""
    
    def __init__(self, base_url: str, max_pages: int = 50):
        """Initialize scraper."""
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.max_pages = max_pages
        self.visited_urls = set()
        self.scraped_pages = []
        self.session = self._create_session()
        
    def _create_session(self):
        """Create session with headers."""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        return session
    
    def fetch_page(self, url: str):
        """Fetch page content."""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}")
            return None
    
    def clean_text(self, text: str) -> str:
        """Clean text content."""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_page_content(self, soup: BeautifulSoup, url: str) -> dict:
        """Extract complete page content."""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        content = {
            'url': url,
            'scraped_at': datetime.now().isoformat(),
        }
        
        # Title
        title = soup.find('title')
        if title:
            content['title'] = self.clean_text(title.get_text())
        else:
            content['title'] = url
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            content['meta_description'] = meta_desc.get('content', '')
        
        # Main heading
        h1 = soup.find('h1')
        if h1:
            content['main_heading'] = self.clean_text(h1.get_text())
        
        # All headings
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            heading_text = self.clean_text(h.get_text())
            if heading_text:
                headings.append({
                    'level': h.name,
                    'text': heading_text
                })
        content['headings'] = headings
        
        # All paragraphs
        paragraphs = []
        for p in soup.find_all('p'):
            para_text = self.clean_text(p.get_text())
            if para_text and len(para_text) > 20:
                paragraphs.append(para_text)
        content['paragraphs'] = paragraphs
        
        # Lists
        lists = []
        for ul in soup.find_all(['ul', 'ol']):
            items = [self.clean_text(li.get_text()) for li in ul.find_all('li')]
            items = [item for item in items if item]
            if items:
                lists.append(items)
        content['lists'] = lists
        
        # Links
        links = []
        for a in soup.find_all('a', href=True):
            link_text = self.clean_text(a.get_text())
            link_url = urljoin(url, a['href'])
            if link_text and link_url:
                links.append({'text': link_text, 'url': link_url})
        content['links'] = links[:50]  # Limit to 50 links
        
        # Images
        images = []
        for img in soup.find_all('img', src=True):
            img_url = urljoin(url, img['src'])
            img_alt = img.get('alt', '')
            images.append({'url': img_url, 'alt': img_alt})
        content['images'] = images[:20]  # Limit to 20 images
        
        # Full text content
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        if main_content:
            content['full_text'] = self.clean_text(main_content.get_text())
        else:
            content['full_text'] = self.clean_text(soup.get_text())
        
        return content
    
    def find_internal_links(self, soup: BeautifulSoup, current_url: str):
        """Find internal links to scrape."""
        links = set()
        for a in soup.find_all('a', href=True):
            url = urljoin(current_url, a['href'])
            parsed = urlparse(url)
            
            # Only same domain
            if parsed.netloc == self.domain:
                # Remove fragments and query params for deduplication
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if clean_url not in self.visited_urls:
                    links.add(clean_url)
        
        return list(links)
    
    def scrape(self):
        """Main scraping method."""
        print("🚀 Starting Full Website Scraper...")
        print(f"📍 Target: {self.base_url}")
        print(f"📄 Max pages: {self.max_pages}\n")
        
        urls_to_visit = [self.base_url]
        
        with tqdm(total=self.max_pages, desc="Scraping pages", unit="page") as pbar:
            while urls_to_visit and len(self.scraped_pages) < self.max_pages:
                current_url = urls_to_visit.pop(0)
                
                if current_url in self.visited_urls:
                    continue
                
                # Fetch page
                soup = self.fetch_page(current_url)
                if not soup:
                    continue
                
                self.visited_urls.add(current_url)
                
                # Extract content
                page_content = self.extract_page_content(soup, current_url)
                self.scraped_pages.append(page_content)
                
                pbar.update(1)
                pbar.set_postfix({"pages": len(self.scraped_pages)})
                
                # Find more links
                if len(self.scraped_pages) < self.max_pages:
                    new_links = self.find_internal_links(soup, current_url)
                    urls_to_visit.extend(new_links[:10])  # Add max 10 new links per page
                
                # Be polite
                time.sleep(1)
        
        print(f"\n✅ Scraping complete!")
        print(f"📊 Total pages scraped: {len(self.scraped_pages)}")
        
        return self.scraped_pages
    
    def generate_html_output(self, pages: list, output_file: str = "scraped_website.html"):
        """Generate beautiful HTML output."""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scraped Website Content - {self.domain}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }}
        
        .stat {{
            background: rgba(255,255,255,0.2);
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        
        .page-card {{
            background: white;
            margin-bottom: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .page-header {{
            background: #667eea;
            color: white;
            padding: 1.5rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .page-header:hover {{
            background: #5568d3;
        }}
        
        .page-number {{
            background: rgba(255,255,255,0.3);
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: bold;
        }}
        
        .page-content {{
            padding: 2rem;
            display: none;
        }}
        
        .page-content.active {{
            display: block;
        }}
        
        .section {{
            margin-bottom: 2rem;
        }}
        
        .section-title {{
            color: #667eea;
            font-size: 1.3rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #667eea;
        }}
        
        .url {{
            color: #666;
            font-size: 0.9rem;
            word-break: break-all;
            background: #f8f9fa;
            padding: 0.5rem;
            border-radius: 5px;
            margin-bottom: 1rem;
        }}
        
        .heading {{
            margin: 0.5rem 0;
            padding-left: 1rem;
        }}
        
        .heading.h1 {{ font-size: 1.8rem; color: #333; }}
        .heading.h2 {{ font-size: 1.5rem; color: #555; }}
        .heading.h3 {{ font-size: 1.3rem; color: #666; }}
        
        .paragraph {{
            margin-bottom: 1rem;
            text-align: justify;
            line-height: 1.8;
        }}
        
        .list {{
            margin: 1rem 0;
            padding-left: 2rem;
        }}
        
        .list li {{
            margin: 0.5rem 0;
        }}
        
        .links-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .link-item {{
            background: #f8f9fa;
            padding: 0.8rem;
            border-radius: 5px;
            border-left: 3px solid #667eea;
        }}
        
        .link-item a {{
            color: #667eea;
            text-decoration: none;
            word-break: break-all;
        }}
        
        .link-item a:hover {{
            text-decoration: underline;
        }}
        
        .full-text {{
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 5px;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 0.9rem;
        }}
        
        .toggle-all {{
            text-align: center;
            margin: 2rem 0;
        }}
        
        .btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.3s;
        }}
        
        .btn:hover {{
            background: #5568d3;
        }}
        
        .export-section {{
            text-align: center;
            margin: 2rem 0;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .export-btn {{
            background: #28a745;
            margin: 0.5rem;
        }}
        
        .export-btn:hover {{
            background: #218838;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🕷️ Scraped Website Content</h1>
        <p><strong>{self.domain}</strong></p>
        <div class="stats">
            <div class="stat">📄 {len(pages)} Pages</div>
            <div class="stat">📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
            <div class="stat">🌐 {self.base_url}</div>
        </div>
    </div>
    
    <div class="container">
        <div class="export-section">
            <h2>📥 Export Options</h2>
            <p>Data is ready for LLM training</p>
            <button class="btn export-btn" onclick="exportJSON()">Export as JSON</button>
            <button class="btn export-btn" onclick="exportText()">Export as Text</button>
        </div>
        
        <div class="toggle-all">
            <button class="btn" onclick="toggleAll()">Expand/Collapse All</button>
        </div>
"""
        
        # Add each page
        for idx, page in enumerate(pages, 1):
            html += f"""
        <div class="page-card">
            <div class="page-header" onclick="togglePage({idx})">
                <div>
                    <span class="page-number">Page {idx}</span>
                    <strong style="margin-left: 1rem;">{page.get('title', 'Untitled')}</strong>
                </div>
                <span id="arrow-{idx}">▼</span>
            </div>
            <div class="page-content" id="page-{idx}">
                <div class="url">🔗 {page['url']}</div>
                
                <div class="section">
                    <div class="section-title">📝 Main Heading</div>
                    <h2>{page.get('main_heading', 'N/A')}</h2>
                </div>
"""
            
            # Headings
            if page.get('headings'):
                html += '<div class="section"><div class="section-title">📋 All Headings</div>'
                for h in page['headings'][:20]:
                    html += f'<div class="heading {h["level"]}">{h["text"]}</div>'
                html += '</div>'
            
            # Paragraphs
            if page.get('paragraphs'):
                html += '<div class="section"><div class="section-title">📄 Content Paragraphs</div>'
                for para in page['paragraphs'][:10]:
                    html += f'<div class="paragraph">{para}</div>'
                html += '</div>'
            
            # Lists
            if page.get('lists'):
                html += '<div class="section"><div class="section-title">📌 Lists</div>'
                for lst in page['lists'][:5]:
                    html += '<ul class="list">'
                    for item in lst[:10]:
                        html += f'<li>{item}</li>'
                    html += '</ul>'
                html += '</div>'
            
            # Links
            if page.get('links'):
                html += '<div class="section"><div class="section-title">🔗 Links Found</div><div class="links-grid">'
                for link in page['links'][:20]:
                    html += f'<div class="link-item"><a href="{link["url"]}" target="_blank">{link["text"]}</a></div>'
                html += '</div></div>'
            
            # Full text
            if page.get('full_text'):
                text_preview = page['full_text'][:2000]
                html += f'<div class="section"><div class="section-title">📖 Full Text Content</div><div class="full-text">{text_preview}...</div></div>'
            
            html += '</div></div>'
        
        html += """
    </div>
    
    <script>
        const pagesData = """ + json.dumps(pages, ensure_ascii=False) + """;
        
        function togglePage(num) {
            const content = document.getElementById('page-' + num);
            const arrow = document.getElementById('arrow-' + num);
            if (content.classList.contains('active')) {
                content.classList.remove('active');
                arrow.textContent = '▼';
            } else {
                content.classList.add('active');
                arrow.textContent = '▲';
            }
        }
        
        function toggleAll() {
            const contents = document.querySelectorAll('.page-content');
            const allExpanded = Array.from(contents).every(c => c.classList.contains('active'));
            contents.forEach(content => {
                if (allExpanded) {
                    content.classList.remove('active');
                } else {
                    content.classList.add('active');
                }
            });
            document.querySelectorAll('[id^="arrow-"]').forEach(arrow => {
                arrow.textContent = allExpanded ? '▼' : '▲';
            });
        }
        
        function exportJSON() {
            const dataStr = JSON.stringify(pagesData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'scraped_data.json';
            link.click();
        }
        
        function exportText() {
            let text = '';
            pagesData.forEach((page, idx) => {
                text += `\\n${'='.repeat(80)}\\n`;
                text += `PAGE ${idx + 1}: ${page.title}\\n`;
                text += `URL: ${page.url}\\n`;
                text += `${'='.repeat(80)}\\n\\n`;
                
                if (page.main_heading) {
                    text += `HEADING: ${page.main_heading}\\n\\n`;
                }
                
                if (page.paragraphs) {
                    text += 'CONTENT:\\n';
                    page.paragraphs.forEach(p => text += p + '\\n\\n');
                }
                
                if (page.full_text) {
                    text += 'FULL TEXT:\\n' + page.full_text + '\\n\\n';
                }
            });
            
            const dataBlob = new Blob([text], {type: 'text/plain'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'scraped_data.txt';
            link.click();
        }
    </script>
</body>
</html>
"""
        
        # Save HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"💾 HTML output saved: {output_file}")
        return output_file


def main():
    """Main function."""
    print("="*60)
    print("🕷️  FULL WEBSITE CONTENT SCRAPER")
    print("="*60)
    print("Complete website scraping for LLM training\n")
    
    # Get URL
    url = input("📍 Enter website URL: ").strip()
    if not url:
        print("❌ URL required!")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Get max pages
    try:
        max_pages_input = input("📄 Max pages to scrape (default: 50): ").strip()
        max_pages = int(max_pages_input) if max_pages_input else 50
    except ValueError:
        max_pages = 50
    
    print(f"\n🚀 Starting scraper...\n")
    
    # Scrape
    scraper = FullWebsiteScraper(url, max_pages=max_pages)
    pages = scraper.scrape()
    
    if pages:
        # Generate HTML
        print("\n📄 Generating HTML output...")
        output_file = scraper.generate_html_output(pages)
        
        # Open in browser
        print(f"\n🌐 Opening in browser...")
        webbrowser.open(f'file://{Path(output_file).absolute()}')
        
        print(f"\n✅ Done!")
        print(f"📊 Scraped {len(pages)} pages")
        print(f"📁 Output: {output_file}")
        print(f"\n💡 You can export data as JSON or TXT from the browser!")
    else:
        print("\n❌ No pages scraped")


if __name__ == "__main__":
    main()























































