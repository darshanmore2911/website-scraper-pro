from datetime import datetime


class MarkdownExporter:
    
    @staticmethod
    def export(pages: list, domain: str, output_file: str = "scraped_content.md") -> str:
        
        md_content = f"""# Scraped Content: {domain}

**Scraped on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Pages:** {len(pages)}

---

"""
        
        md_content += "## 📑 Table of Contents\n\n"
        for idx, page in enumerate(pages, 1):
            title = page.get('title', 'Untitled')
            md_content += f"{idx}. [{title}](#{idx}-{title.lower().replace(' ', '-')})\n"
        
        md_content += "\n---\n\n"
        
        for idx, page in enumerate(pages, 1):
            title = page.get('title', 'Untitled')
            url = page.get('url', '')
            
            md_content += f"## {idx}. {title}\n\n"
            md_content += f"**URL:** [{url}]({url})\n\n"
            
            if page.get('main_heading'):
                md_content += f"### {page['main_heading']}\n\n"
            
            if page.get('meta_description'):
                md_content += f"> {page['meta_description']}\n\n"
            
            if page.get('headings'):
                md_content += "#### Headings:\n\n"
                for h in page['headings'][:10]:
                    level = int(h['level'][1])
                    md_content += f"{'  ' * (level-1)}- {h['text']}\n"
                md_content += "\n"
            
            if page.get('paragraphs'):
                md_content += "#### Content:\n\n"
                for para in page['paragraphs'][:5]:
                    md_content += f"{para}\n\n"
            
            if page.get('lists'):
                md_content += "#### Lists:\n\n"
                for lst in page['lists'][:3]:
                    for item in lst[:10]:
                        md_content += f"- {item}\n"
                    md_content += "\n"
            
            md_content += "---\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return output_file
