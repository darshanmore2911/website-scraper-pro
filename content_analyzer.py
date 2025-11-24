from collections import Counter
import re


class ContentAnalyzer:
    
    @staticmethod
    def analyze_pages(pages: list) -> dict:
        stats = {
            'total_pages': len(pages),
            'total_words': 0,
            'total_paragraphs': 0,
            'total_headings': 0,
            'total_links': 0,
            'total_images': 0,
            'avg_words_per_page': 0,
            'top_keywords': [],
            'reading_time_minutes': 0,
        }
        
        all_words = []
        
        for page in pages:
            full_text = page.get('full_text', '')
            words = re.findall(r'\b\w+\b', full_text.lower())
            all_words.extend(words)
            stats['total_words'] += len(words)
            
            stats['total_paragraphs'] += len(page.get('paragraphs', []))
            stats['total_headings'] += len(page.get('headings', []))
            stats['total_links'] += len(page.get('links', []))
            stats['total_images'] += len(page.get('images', []))
        
        if stats['total_pages'] > 0:
            stats['avg_words_per_page'] = stats['total_words'] // stats['total_pages']
            stats['reading_time_minutes'] = stats['total_words'] // 200
        
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                     'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
                     'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
        
        filtered_words = [w for w in all_words if w not in stop_words and len(w) > 3]
        word_counts = Counter(filtered_words)
        stats['top_keywords'] = word_counts.most_common(20)
        
        return stats
