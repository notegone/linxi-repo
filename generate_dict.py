import jieba
import os

def generate_dict_file():
    """Generate a dictionary file from jieba's default dict and custom words."""
    # Get jieba's default dictionary path
    default_dict_path = os.path.join(os.path.dirname(jieba.__file__), 'dict.txt')
    
    # Create a set to store unique words with their weights
    word_weights = {}
    
    # Read jieba's default dictionary
    with open(default_dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                word = parts[0]
                try:
                    freq = int(parts[1])
                    # Convert frequency to a relative weight (1-10 scale)
                    weight = min(10, max(1, int(freq / 1000000)))
                    word_weights[word] = weight
                except ValueError:
                    continue

    # Write our custom dictionary
    with open('docs/dict.txt', 'w', encoding='utf-8') as f:
        # First write some common music-related terms with high weights
        music_terms = {
            '歌詞': 10,
            '副歌': 10,
            '主歌': 10,
            '前奏': 10,
            '間奏': 10,
            '結尾': 10,
            '伴奏': 10,
            '和音': 9,
            '旋律': 9,
            '節奏': 9,
            '音樂': 10,
            '歌手': 10,
            '樂隊': 9,
            '演唱': 9,
            '合唱': 9,
            '獨唱': 9,
        }
        
        # Write music terms first
        for word, weight in music_terms.items():
            f.write(f'{word} {weight}\n')
        
        # Then write words from jieba's dictionary that are 2 or more characters
        for word, weight in word_weights.items():
            if len(word) >= 2:  # Only include words with 2 or more characters
                f.write(f'{word} {weight}\n')

if __name__ == '__main__':
    # Create docs directory if it doesn't exist
    os.makedirs('docs', exist_ok=True)
    
    # Generate the dictionary file
    generate_dict_file()
    print("Dictionary file generated at docs/dict.txt")
