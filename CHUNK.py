"""
STEP 1: SEMANTIC CHUNKING FOR PROPHET'S WIVES DATA
Creates intelligent chunks that preserve context and meaning
"""

import json
import re
from typing import List, Dict

# ============================================
# SEMANTIC CHUNKER CLASS
# ============================================

class SemanticChunker:
    """Creates semantically meaningful chunks from wife biographies"""
    
    def __init__(self, max_chunk_size=800, min_chunk_size=400):
        """
        Initialize chunker with size constraints
        
        Args:
            max_chunk_size: Maximum characters per chunk (default: 800)
            min_chunk_size: Minimum characters per chunk (default: 400)
        """
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        
        print(f"✅ Chunker initialized:")
        print(f"   - Max chunk size: {max_chunk_size} chars (~{max_chunk_size//6} words)")
        print(f"   - Min chunk size: {min_chunk_size} chars (~{min_chunk_size//6} words)")
    
    def extract_wife_info(self, text: str) -> Dict:
        """
        Extract wife name and aliases from text
        This helps in identifying which wife the chunk belongs to
        """
        wife_name = None
        aliases = []
        
        # IMPROVED: Better pattern to capture full name including 3 parts
        # Pattern: "umm al-muminin NAME bint FATHER_NAME"
        name_match = re.search(
            r'umm al-muminin\s+([a-z]+(?:\s+bint\s+[a-z]+(?:\s+[a-z]+)?)?)',
            text.lower()
        )
        if name_match:
            wife_name = name_match.group(1).title()
        
        # IMPROVED: Better alias extraction (only short names, not sentences)
        alias_patterns = [
            r'also known as[:\s]+([a-z\s]{3,20})(?:[,\.]|$)',
            r'nicknamed[:\s]+([a-z\s]{3,20})(?:[,\.]|$)',
            r'called[:\s]+([a-z\s]{3,20})(?:[,\.]|$)',
            r'dubbed[:\s]+([a-z\s]{3,20})(?:[,\.]|$)',
        ]
        
        for pattern in alias_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                # Clean and validate alias
                alias = match.strip()
                # Only keep if it's a reasonable name (3-20 chars, mostly letters)
                if 3 <= len(alias) <= 20 and sum(c.isalpha() for c in alias) > len(alias) * 0.7:
                    aliases.append(alias.title())
        
        return {
            'wife_name': wife_name,
            'aliases': list(set(aliases))  # Remove duplicates
        }
    
    def split_into_sections(self, text: str) -> List[Dict]:
        """
        Split text into semantic sections based on topics
        This preserves context by keeping related information together
        """
        sections = []
        
        # Define section headers (topics commonly found in biographies)
        section_markers = [
            'name and lineage',
            'her marriage',
            'her life with',
            'her emigration',
            'her death',
            'her virtues',
            'embracing islam',
            'her childhood',
            'her upbringing',
            'her knowledge',
            'wisdom behind',
            'her contributions',
            'her generosity',
            'battle of',
            'her worship',
            'her piety',
            'criteria for',
            'the wisdom',
            'her father',
            'her mother'
        ]
        
        # Split by double newlines (paragraphs)
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        current_section = {
            'title': 'Introduction',
            'content': []
        }
        
        for para in paragraphs:
            # Check if paragraph starts a new section
            para_lower = para.lower()
            is_new_section = False
            
            for marker in section_markers:
                if para_lower.startswith(marker):
                    # Save previous section if it has content
                    if current_section['content']:
                        sections.append(current_section)
                    
                    # Start new section
                    current_section = {
                        'title': marker.title(),
                        'content': [para]
                    }
                    is_new_section = True
                    break
            
            if not is_new_section:
                current_section['content'].append(para)
        
        # Add last section
        if current_section['content']:
            sections.append(current_section)
        
        return sections
    
    def create_chunks(self, chapter_text: str) -> List[Dict]:
        """
        Create semantic chunks with rich metadata
        
        Returns:
            List of chunks with structure:
            {
                'wife_name': str,
                'aliases': list,
                'section': str,
                'content': str,
                'char_count': int
            }
        """
        chunks = []
        
        # Step 1: Extract wife information
        wife_info = self.extract_wife_info(chapter_text)
        
        # Step 2: Split into sections
        sections = self.split_into_sections(chapter_text)
        
        # Step 3: Create chunks from sections
        for section in sections:
            section_text = ' '.join(section['content'])
            
            # If section is small enough, keep as one chunk
            if len(section_text) <= self.max_chunk_size:
                chunks.append({
                    'wife_name': wife_info['wife_name'] or 'Unknown',
                    'aliases': wife_info['aliases'],
                    'section': section['title'],
                    'content': section_text,
                    'char_count': len(section_text)
                })
            else:
                # Split large sections by sentences
                sentences = re.split(r'(?<=[.!?])\s+', section_text)
                
                current_chunk = []
                current_length = 0
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                        
                    sentence_length = len(sentence)
                    
                    # If adding this sentence exceeds max, save current chunk
                    if current_length + sentence_length > self.max_chunk_size and current_length >= self.min_chunk_size:
                        chunk_content = ' '.join(current_chunk)
                        chunks.append({
                            'wife_name': wife_info['wife_name'] or 'Unknown',
                            'aliases': wife_info['aliases'],
                            'section': section['title'],
                            'content': chunk_content,
                            'char_count': len(chunk_content)
                        })
                        current_chunk = [sentence]
                        current_length = sentence_length
                    else:
                        current_chunk.append(sentence)
                        current_length += sentence_length + 1  # +1 for space
                
                # Add remaining chunk
                if current_chunk:
                    chunk_content = ' '.join(current_chunk)
                    chunks.append({
                        'wife_name': wife_info['wife_name'] or 'Unknown',
                        'aliases': wife_info['aliases'],
                        'section': section['title'],
                        'content': chunk_content,
                        'char_count': len(chunk_content)
                    })
        
        return chunks

# ============================================
# PROCESSING FUNCTION
# ============================================

def process_chapters(input_file: str, output_file: str):
    """
    Process chapter-wise data into semantic chunks
    
    Args:
        input_file: Path to chpWise.json
        output_file: Path to save semantic_chunks.json
    """
    
    print("\n" + "="*70)
    print("🌙 SEMANTIC CHUNKING FOR PROPHET'S WIVES DATA")
    print("="*70)
    
    # Load chapter data
    print(f"\n📚 Loading data from: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            chapters = json.load(f)
        print(f"✅ Loaded {len(chapters)} chapters")
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found!")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: File '{input_file}' is not valid JSON!")
        return
    
    # Initialize chunker
    print("\n🔧 Initializing semantic chunker...")
    chunker = SemanticChunker(max_chunk_size=800, min_chunk_size=400)
    
    # Process each chapter
    print("\n✂️  Creating semantic chunks...")
    print("-" * 70)
    
    all_chunks = []
    wife_chunk_counts = {}
    
    for i, chapter in enumerate(chapters, 1):
        print(f"\n📖 Processing chapter {i}/{len(chapters)}...")
        
        chapter_chunks = chunker.create_chunks(chapter)
        all_chunks.extend(chapter_chunks)
        
        # Track chunks per wife
        if chapter_chunks:
            wife_name = chapter_chunks[0]['wife_name']
            wife_chunk_counts[wife_name] = len(chapter_chunks)
            print(f"   ✅ Created {len(chapter_chunks)} chunks for {wife_name}")
    
    # POST-PROCESSING: Fix "Unknown" and incomplete names
    print("\n🔧 Post-processing: Fixing incomplete names...")
    
    # Manual mapping for known wives (based on table of contents)
    wife_mappings = {
        'umm salamah hind': 'Umm Salamah Hind Bint Umayyah',
        'umm habibah ramlah': 'Umm Habibah Ramlah Bint Abu Sufyan',
    }
    
    fixed_count = 0
    for chunk in all_chunks:
        # Fix incomplete "Umm" names by checking content
        if chunk['wife_name'] == 'Umm' or chunk['wife_name'] == 'Unknown':
            content_lower = chunk['content'].lower()
            
            # Check for specific patterns in content
            if 'umm salamah' in content_lower:
                chunk['wife_name'] = 'Umm Salamah Hind Bint Umayyah'
                fixed_count += 1
            elif 'umm habibah' in content_lower:
                chunk['wife_name'] = 'Umm Habibah Ramlah Bint Abu Sufyan'
                fixed_count += 1
            elif 'conclusion' in content_lower:
                chunk['wife_name'] = 'Conclusion'
                chunk['section'] = 'Conclusion'
                fixed_count += 1
    
    print(f"✅ Fixed {fixed_count} chunks with incomplete/unknown names")
    
    # Recalculate statistics after fixing
    wife_chunk_counts = {}
    for chunk in all_chunks:
        wife_name = chunk['wife_name']
        wife_chunk_counts[wife_name] = wife_chunk_counts.get(wife_name, 0) + 1
    
    # Display statistics
    print("\n" + "="*70)
    print("📊 CHUNKING STATISTICS")
    print("="*70)
    print(f"Total chunks created: {len(all_chunks)}")
    print(f"\nChunks per wife:")
    for wife, count in sorted(wife_chunk_counts.items()):
        print(f"  - {wife}: {count} chunks")
    
    # Calculate average chunk size
    avg_size = sum(c['char_count'] for c in all_chunks) / len(all_chunks)
    print(f"\nAverage chunk size: {int(avg_size)} characters (~{int(avg_size/6)} words)")
    
    # Show size distribution
    small_chunks = sum(1 for c in all_chunks if c['char_count'] < 500)
    medium_chunks = sum(1 for c in all_chunks if 500 <= c['char_count'] < 800)
    large_chunks = sum(1 for c in all_chunks if c['char_count'] >= 800)
    
    print(f"\nSize distribution:")
    print(f"  - Small (<500 chars): {small_chunks}")
    print(f"  - Medium (500-800 chars): {medium_chunks}")
    print(f"  - Large (≥800 chars): {large_chunks}")
    
    # Quality checks
    print(f"\n🔍 Quality checks:")
    unknown_chunks = sum(1 for c in all_chunks if c['wife_name'] == 'Unknown')
    if unknown_chunks > 0:
        print(f"  ⚠️  Warning: {unknown_chunks} chunks still have 'Unknown' wife name")
    else:
        print(f"  ✅ All chunks have identified wife names")
    
    # Save chunks
    print(f"\n💾 Saving chunks to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    
    print("✅ Chunks saved successfully!")
    
    # Show sample chunk
    print("\n" + "="*70)
    print("📝 SAMPLE CHUNK (First chunk)")
    print("="*70)
    if all_chunks:
        sample = all_chunks[0]
        print(f"Wife: {sample['wife_name']}")
        print(f"Section: {sample['section']}")
        print(f"Aliases: {sample['aliases']}")
        print(f"Character count: {sample['char_count']}")
        print(f"\nContent preview (first 300 chars):")
        print("-" * 70)
        print(sample['content'][:300] + "...")
    
    print("\n" + "="*70)
    print("✨ CHUNKING COMPLETE!")
    print("="*70)
    print(f"\n📁 Output file: {output_file}")
    print("📊 Next steps:")
    print("  1. Review the chunks in 'semantic_chunks.json'")
    print("  2. Check if wife names are correctly identified")
    print("  3. Verify sections are properly separated")
    print("  4. Ready for embedding generation!")
    
    return all_chunks

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    # Run chunking process
    chunks = process_chapters(
        input_file='chpWise.json',
        output_file='semantic_chunks.json'
    )
    
    print("\n🎉 Done! Check 'semantic_chunks.json' to see the results.")
