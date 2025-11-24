"""Simple HTML Generator - No AI, No PDF"""

from datetime import datetime
import json


def generate_html(pages: list, domain: str, stats: dict, base_url: str, 
                 output_file: str = "scraped_website.html") -> str:
    """Generate clean HTML with search and export."""
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scraped Content - {domain}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
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
            position: sticky;
            top: 0;
            z-index: 1000;
        }}
        
        .header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.2);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
        }}
        
        .stat-number {{ font-size: 2rem; font-weight: bold; display: block; }}
        .stat-label {{ font-size: 0.9rem; opacity: 0.9; }}
        
        .search-bar {{
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        
        .search-input {{
            width: 100%;
            padding: 1rem;
            font-size: 1.1rem;
            border: 2px solid #667eea;
            border-radius: 10px;
            outline: none;
        }}
        
        .search-input:focus {{
            border-color: #764ba2;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        }}
        
        .search-results {{
            margin: 1rem 0;
            padding: 1rem;
            background: white;
            border-radius: 10px;
            display: none;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        
        .export-section {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .export-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s;
            width: 100%;
        }}
        
        .btn:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }}
        
        .btn-success {{ background: #28a745; }}
        .btn-success:hover {{ background: #218838; }}
        
        .btn-info {{ background: #17a2b8; }}
        .btn-info:hover {{ background: #138496; }}
        
        .analysis-section {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .keywords-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 0.5rem;
            margin-top: 1rem;
        }}
        
        .keyword-tag {{
            background: #f0f0f0;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            text-align: center;
            border-left: 3px solid #667eea;
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
        
        .page-header:hover {{ background: #5568d3; }}
        
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
        
        .page-content.active {{ display: block; }}
        
        .section {{ margin-bottom: 2rem; }}
        
        .section-title {{
            color: #667eea;
            font-size: 1.3rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #667eea;
        }}
        
        .highlight {{
            background-color: yellow;
            padding: 2px 4px;
            border-radius: 3px;
            font-weight: bold;
            color: #000;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🕷️ Website Scraper</h1>
        <p><strong>{domain}</strong></p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">
            Developed by <a href="https://github.com/darshanmore2911" target="_blank" 
            style="color: white; text-decoration: underline;">Darshan More</a>
        </p>
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-number">{stats['total_pages']}</span>
                <span class="stat-label">Pages</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{stats['total_words']:,}</span>
                <span class="stat-label">Words</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{stats['reading_time_minutes']}</span>
                <span class="stat-label">Min Read</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{stats['total_headings']}</span>
                <span class="stat-label">Headings</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{stats['total_links']}</span>
                <span class="stat-label">Links</span>
            </div>
        </div>
    </div>
    
    <div class="search-bar">
        <input type="text" class="search-input" id="searchInput" 
               placeholder="🔍 Search content..." onkeyup="searchContent()">
        <div class="search-results" id="searchResults"></div>
    </div>
    
    <div class="container">
        <div class="export-section">
            <h2>📥 Export Options</h2>
            <p>Download scraped content in various formats</p>
            <div class="export-grid">
                <button class="btn btn-success" onclick="exportJSON()">📄 Export JSON</button>
                <button class="btn btn-info" onclick="exportText()">📝 Export TXT</button>
                <button class="btn" onclick="exportMarkdown()">📋 Export Markdown</button>
            </div>
        </div>
        
        <div class="analysis-section">
            <h2>📊 Content Analysis</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-number">{stats['total_paragraphs']}</span>
                    <span class="stat-label">Paragraphs</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{stats['avg_words_per_page']}</span>
                    <span class="stat-label">Avg Words/Page</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{stats['total_images']}</span>
                    <span class="stat-label">Images</span>
                </div>
            </div>
            
            <h3 style="margin-top: 2rem; color: #667eea;">🔑 Top Keywords</h3>
            <div class="keywords-grid">
"""
    
    # Add keywords
    for keyword, count in stats['top_keywords'][:15]:
        html += f'<div class="keyword-tag"><strong>{keyword}</strong> ({count})</div>'
    
    html += """
            </div>
        </div>
        
        <div style="text-align: center; margin: 2rem 0;">
            <button class="btn" onclick="toggleAll()">Expand/Collapse All</button>
        </div>
"""
    
    # Add pages
    for idx, page in enumerate(pages, 1):
        html += f"""
        <div class="page-card" data-page-id="{idx}">
            <div class="page-header" onclick="togglePage({idx})">
                <div>
                    <span class="page-number">Page {idx}</span>
                    <strong style="margin-left: 1rem;">{page.get('title', 'Untitled')}</strong>
                </div>
                <span id="arrow-{idx}">▼</span>
            </div>
            <div class="page-content" id="page-{idx}">
                <div class="section">
                    <div class="section-title">🔗 URL</div>
                    <a href="{page['url']}" target="_blank">{page['url']}</a>
                </div>
"""
        
        if page.get('main_heading'):
            html += f"""
                <div class="section">
                    <div class="section-title">📝 Main Heading</div>
                    <h2>{page['main_heading']}</h2>
                </div>
"""
        
        if page.get('paragraphs'):
            html += '<div class="section"><div class="section-title">📄 Content</div>'
            for para in page['paragraphs'][:10]:
                html += f'<p style="margin-bottom: 1rem;">{para}</p>'
            html += '</div>'
        
        html += '</div></div>'
    
    html += """
    </div>
    
    <footer style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; padding: 2rem; text-align: center; margin-top: 3rem;">
        <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
            <strong>🕷️ Website Scraper Pro</strong>
        </p>
        <p style="font-size: 0.9rem; opacity: 0.9;">
            Developed with ❤️ by 
            <a href="https://github.com/darshanmore2911" target="_blank" 
               style="color: white; text-decoration: underline; font-weight: bold;">
                Darshan More
            </a>
        </p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.8;">
            <a href="https://github.com/darshanmore2911" target="_blank" 
               style="color: white; text-decoration: none;">
                GitHub
            </a> • 
            <a href="https://www.linkedin.com/in/darshanmore29" target="_blank" 
               style="color: white; text-decoration: none;">
                LinkedIn
            </a> • 
            <a href="https://www.instagram.com/itzdarshann" target="_blank" 
               style="color: white; text-decoration: none;">
                Instagram
            </a>
        </p>
        <p style="font-size: 0.75rem; margin-top: 1rem; opacity: 0.7;">
            © 2025 Darshan More. All rights reserved.
        </p>
    </footer>
    
    <script>
        const pagesData = """ + json.dumps(pages, ensure_ascii=False) + """;
        let currentSearchQuery = '';
        
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
        
        function removeHighlights() {
            document.querySelectorAll('.highlight').forEach(el => {
                const parent = el.parentNode;
                parent.replaceChild(document.createTextNode(el.textContent), el);
                parent.normalize();
            });
        }
        
        function highlightText(element, query) {
            if (!query || query.length < 3) return;
            
            const walker = document.createTreeWalker(
                element,
                NodeFilter.SHOW_TEXT,
                null,
                false
            );
            
            const nodesToReplace = [];
            let node;
            
            while (node = walker.nextNode()) {
                if (node.parentElement.classList.contains('highlight')) continue;
                if (node.parentElement.tagName === 'SCRIPT') continue;
                if (node.parentElement.tagName === 'STYLE') continue;
                
                const text = node.textContent;
                const lowerText = text.toLowerCase();
                const lowerQuery = query.toLowerCase();
                
                if (lowerText.includes(lowerQuery)) {
                    nodesToReplace.push(node);
                }
            }
            
            nodesToReplace.forEach(node => {
                const text = node.textContent;
                const lowerText = text.toLowerCase();
                const lowerQuery = query.toLowerCase();
                
                const parts = [];
                let lastIndex = 0;
                let index = lowerText.indexOf(lowerQuery);
                
                while (index !== -1) {
                    if (index > lastIndex) {
                        parts.push(document.createTextNode(text.substring(lastIndex, index)));
                    }
                    
                    const span = document.createElement('span');
                    span.className = 'highlight';
                    span.textContent = text.substring(index, index + query.length);
                    parts.push(span);
                    
                    lastIndex = index + query.length;
                    index = lowerText.indexOf(lowerQuery, lastIndex);
                }
                
                if (lastIndex < text.length) {
                    parts.push(document.createTextNode(text.substring(lastIndex)));
                }
                
                const parent = node.parentNode;
                parts.forEach(part => parent.insertBefore(part, node));
                parent.removeChild(node);
            });
        }
        
        function searchContent() {
            const query = document.getElementById('searchInput').value.trim();
            const results = document.getElementById('searchResults');
            
            removeHighlights();
            
            if (query.length < 3) {
                results.style.display = 'none';
                currentSearchQuery = '';
                return;
            }
            
            currentSearchQuery = query;
            results.style.display = 'block';
            results.innerHTML = '<h3>Searching...</h3>';
            
            let found = 0;
            const matchingPages = [];
            
            pagesData.forEach((page, idx) => {
                const title = (page.title || '').toLowerCase();
                const text = (page.full_text || '').toLowerCase();
                const queryLower = query.toLowerCase();
                
                if (title.includes(queryLower) || text.includes(queryLower)) {
                    found++;
                    const occurrences = (text.match(new RegExp(queryLower, 'g')) || []).length;
                    matchingPages.push({
                        idx: idx + 1,
                        title: page.title,
                        occurrences: occurrences
                    });
                }
            });
            
            if (found === 0) {
                results.innerHTML = '<h3>No results found</h3><p>Try different keywords</p>';
            } else {
                results.innerHTML = `<h3>Found ${found} pages with "${query}"</h3>`;
                matchingPages.forEach(match => {
                    results.innerHTML += `
                        <div style="padding: 1rem; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>Page ${match.idx}:</strong> ${match.title}
                                <br><small style="color: #666;">${match.occurrences} occurrence(s)</small>
                            </div>
                            <button onclick="scrollToPageAndHighlight(${match.idx})" 
                                    style="padding: 0.5rem 1rem; 
                                           background: #667eea; color: white; border: none; 
                                           border-radius: 5px; cursor: pointer; white-space: nowrap;">
                                View & Highlight
                            </button>
                        </div>
                    `;
                });
            }
        }
        
        function scrollToPageAndHighlight(num) {
            const page = document.querySelector(`[data-page-id="${num}"]`);
            const content = document.getElementById('page-' + num);
            
            if (!content.classList.contains('active')) {
                togglePage(num);
            }
            
            setTimeout(() => {
                page.scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                setTimeout(() => {
                    if (currentSearchQuery) {
                        highlightText(content, currentSearchQuery);
                        
                        const firstHighlight = content.querySelector('.highlight');
                        if (firstHighlight) {
                            firstHighlight.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        }
                    }
                }, 300);
            }, 100);
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
            });
            
            const dataBlob = new Blob([text], {type: 'text/plain'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'scraped_data.txt';
            link.click();
        }
        
        function exportMarkdown() {
            let md = `# Scraped Content\\n\\n`;
            md += `**Domain:** """ + domain + """\\n`;
            md += `**Date:** ${new Date().toLocaleDateString()}\\n\\n`;
            md += `---\\n\\n`;
            
            pagesData.forEach((page, idx) => {
                md += `## ${idx + 1}. ${page.title}\\n\\n`;
                md += `**URL:** [${page.url}](${page.url})\\n\\n`;
                
                if (page.main_heading) {
                    md += `### ${page.main_heading}\\n\\n`;
                }
                
                if (page.paragraphs) {
                    page.paragraphs.forEach(p => md += `${p}\\n\\n`);
                }
                
                md += `---\\n\\n`;
            });
            
            const dataBlob = new Blob([md], {type: 'text/markdown'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'scraped_data.md';
            link.click();
        }
    </script>
</body>
</html>
"""
    
    # Save file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_file
