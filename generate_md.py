import json
import os
import re
from urllib.parse import urlparse, parse_qs
import html

def sanitize_filename(filename):
    """Convert a string to a safe filename."""
    filename = filename.lower()
    filename = re.sub(r'[/\\?%*:|"<>\(\)\{\}\[\].,;\s]', '-', filename)
    filename = ''.join(char for char in filename
                      if ('\u4e00' <= char <= '\u9fff') or  
                      char.isascii() and char.isprintable())
    filename = re.sub('-+', '-', filename)
    filename = filename.strip('-')
    return filename

def get_youtube_embed_url(youtube_url):
    """Convert YouTube URL to embed URL."""
    parsed = urlparse(youtube_url)
    if 'youtube.com' in parsed.netloc:
        video_id = parse_qs(parsed.query).get('v', [None])[0]
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
    return None

def create_vocabulary_table(vocabulary):
    """Create a markdown table for vocabulary."""
    table = "| Word | Pinyin | Jyutping | English Definition |\n"
    table += "|------|---------|-----------|-------------------|\n"
    for item in vocabulary:
        table += f"| {item['word']} | {item['pinyin']} | {item['jyutping']} | {item['english_definition']} |\n"
    return table

def highlight_vocabulary_in_lyrics(lyrics, vocabulary):
    """Highlight vocabulary words in lyrics using HTML spans."""
    highlighted_lyrics = lyrics
    
    # Sort vocabulary by word length (longest first) to avoid partial word replacements
    sorted_vocab = sorted(vocabulary, key=lambda x: len(x['word']), reverse=True)
    
    for item in sorted_vocab:
        word = item['word']
        # Escape the content for the tooltip
        tooltip_content = html.escape(f"{item['pinyin']} | {item['jyutping']} | {item['english_definition']}")
        # Create HTML span with data attribute for tooltip
        span = f'<span class="vocab-word" data-tooltip="{tooltip_content}">{word}</span>'
        # Replace the word with the span
        highlighted_lyrics = highlighted_lyrics.replace(word, span)
    
    # Convert newlines to <br> tags for HTML display
    highlighted_lyrics = highlighted_lyrics.replace('\n', '<br>\n')
    
    return highlighted_lyrics

def generate_markdown_files(json_data):
    """Generate markdown files from JSON data."""
    # Create docs directory if it doesn't exist
    os.makedirs("docs", exist_ok=True)
    
    # Generate index.md
    with open("docs/index.md", "w", encoding="utf-8") as f:
        f.write("# Chinese Songs Lyrics Collection\n\n")
        f.write("Welcome to the Chinese Songs Lyrics Collection! This site contains lyrics and vocabulary from various Chinese songs to help you learn Chinese through music.\n\n")
        f.write("## Available Songs\n\n")
        
        for song in json_data:
            safe_filename = sanitize_filename(song['name'])
            f.write(f"* [{song['name']}]({safe_filename}.md)\n")

    # Generate individual song pages
    for song in json_data:
        safe_filename = sanitize_filename(song['name'])
        
        with open(f"docs/{safe_filename}.md", "w", encoding="utf-8") as f:
            # Write song title
            f.write(f"# {song['name']}\n\n")
            
            # Add YouTube embed if available
            embed_url = get_youtube_embed_url(song['youtube_url'])
            if embed_url:
                f.write(f'<div class="video-container">\n')
                f.write(f'<iframe width="100%" height="400" src="{embed_url}" frameborder="0" allowfullscreen></iframe>\n')
                f.write('</div>\n\n')
            
            # Add lyrics section with highlighted vocabulary
            f.write("## Lyrics\n\n")
            highlighted_lyrics = highlight_vocabulary_in_lyrics(song['lyrics'], song['vocabulary'])
            f.write('<div class="lyrics-container">\n')
            f.write(highlighted_lyrics)
            f.write('\n</div>\n\n')
            
            # Add vocabulary section
            f.write("## Vocabulary\n\n")
            f.write(create_vocabulary_table(song['vocabulary']))

def main():
    # Read JSON data
    with open("songs.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    
    # Generate markdown files
    generate_markdown_files(json_data)

if __name__ == "__main__":
    main()
