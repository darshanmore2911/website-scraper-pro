"""
Website Scraper Pro
Developed by Darshan More
GitHub: https://github.com/darshanmore2911
"""

from full_website_scraper import FullWebsiteScraper
from content_analyzer import ContentAnalyzer
from markdown_exporter import MarkdownExporter
from simple_html_generator import generate_html
import webbrowser
from pathlib import Path


def main():
    print("="*60)
    print("🚀 WEBSITE SCRAPER PRO")
    print("="*60)
    print("Features: Search | Analysis | Multi-Export\n")
    
    url = input("📍 Enter website URL: ").strip()
    if not url:
        print("❌ URL required!")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        max_pages_input = input("📄 Max pages (default: 50): ").strip()
        max_pages = int(max_pages_input) if max_pages_input else 50
    except ValueError:
        max_pages = 50
    
    print(f"\n🚀 Starting scraper...\n")
    
    print("📥 Step 1/4: Scraping website...")
    scraper = FullWebsiteScraper(url, max_pages=max_pages)
    pages = scraper.scrape()
    
    if not pages:
        print("\n❌ No pages scraped")
        return
    
    print("\n📊 Step 2/4: Analyzing content...")
    analyzer = ContentAnalyzer()
    stats = analyzer.analyze_pages(pages)
    
    print(f"  ✅ Total words: {stats['total_words']:,}")
    print(f"  ✅ Reading time: {stats['reading_time_minutes']} minutes")
    print(f"  ✅ Top keyword: {stats['top_keywords'][0][0] if stats['top_keywords'] else 'N/A'}")
    
    print("\n📁 Step 3/4: Generating exports...")
    
    try:
        md_file = MarkdownExporter.export(pages, scraper.domain)
        print(f"  ✅ Markdown: {md_file}")
    except Exception as e:
        print(f"  ⚠️  Markdown export failed: {e}")
    
    print("\n🌐 Step 4/4: Generating interactive HTML...")
    try:
        html_file = generate_html(pages, scraper.domain, stats, url)
        print(f"  ✅ HTML: {html_file}")
        
        print(f"\n🌐 Opening in browser...")
        webbrowser.open(f'file://{Path(html_file).absolute()}')
        
    except Exception as e:
        print(f"  ❌ HTML generation failed: {e}")
        return
    
    print("\n" + "="*60)
    print("✅ COMPLETE!")
    print("="*60)
    print(f"\n📊 Statistics:")
    print(f"  • Pages scraped: {len(pages)}")
    print(f"  • Total words: {stats['total_words']:,}")
    print(f"  • Reading time: {stats['reading_time_minutes']} minutes")
    print(f"  • Headings: {stats['total_headings']}")
    print(f"  • Links: {stats['total_links']}")
    
    print(f"\n📁 Files generated:")
    print(f"  • {html_file} (Interactive HTML)")
    print(f"  • scraped_content.md (Markdown)")
    
    print(f"\n💡 From the browser you can:")
    print(f"  • 🔍 Search content")
    print(f"  • 📥 Export as JSON/TXT/Markdown")
    print(f"  • 📊 View analysis & keywords")
    
    print(f"\n🎉 Done! Check your browser!")


if __name__ == "__main__":
    main()
