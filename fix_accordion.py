# -*- coding: utf-8 -*-
"""Extract domain/topic data from Google Sheet and hardcode into domain_prompts.py"""

import requests
import pandas as pd
import os
import shutil

def extract_from_google_sheet():
    """Extract data from Google Sheet"""
    
    # Google Sheet URL (published as CSV)
    sheet_id = "1ohiL6xOBbjC7La2iUdkjrVjG4IEUnVWhI0fRoarD6P0"
    gid = "1507296519"
    
    # Try to read as CSV export
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    print(f"📥 Fetching data from Google Sheet...")
    print(f"   URL: {csv_url}\n")
    
    try:
        # Read CSV
        df = pd.read_csv(csv_url)
        
        print(f"✅ Successfully loaded {len(df)} rows\n")
        print("📊 Preview:")
        print(df.head(10))
        print("\n" + "=" * 80 + "\n")
        
        # Build DOMAIN_PROMPTS dictionary
        domain_prompts = {}
        
        # Assuming columns: Domain | Topic | System Prompt
        # Adjust column names based on actual sheet structure
        for _, row in df.iterrows():
            # Try different possible column names
            domain = None
            topic = None
            prompt = None
            
            # Try to find domain column
            for col in df.columns:
                if 'lĩnh vực' in col.lower() or 'domain' in col.lower() or 'linh vuc' in col.lower():
                    domain = str(row[col]).strip()
                elif 'chủ đề' in col.lower() or 'topic' in col.lower() or 'chu de' in col.lower():
                    topic = str(row[col]).strip()
                elif 'prompt' in col.lower() or 'system' in col.lower() or 'mô tả' in col.lower():
                    prompt = str(row[col]).strip()
            
            # Skip if any field is empty or NaN
            if not domain or domain == 'nan' or not topic or topic == 'nan':
                continue
            
            # Add to dictionary
            if domain not in domain_prompts:
                domain_prompts[domain] = {}
            
            domain_prompts[domain][topic] = prompt if prompt and prompt != 'nan' else ""
        
        print(f"✅ Extracted {len(domain_prompts)} domains")
        for domain, topics in domain_prompts.items():
            print(f"   • {domain}: {len(topics)} topics")
        
        return domain_prompts
        
    except Exception as e:
        print(f"❌ Error reading Google Sheet: {e}")
        print("\n⚠️  Sheet might not be published or accessible")
        print("\nPlease ensure:")
        print("  1. Sheet is published to web (File → Share → Publish to web)")
        print("  2. Sheet is set to 'Anyone with link can view'")
        return None

def generate_domain_prompts_file(domain_prompts):
    """Generate domain_prompts.py file with hardcoded data"""
    
    file_path = os.path.join("services", "domain_prompts.py")
    
    # Backup existing file
    if os.path.exists(file_path):
        backup = file_path + '.backup_before_sheet_extract'
        shutil.copy2(file_path, backup)
        print(f"\n✅ Backup: {backup}")
    
    # Generate Python code
    code = '''# -*- coding: utf-8 -*-
"""
Domain-specific system prompts for video generation
Auto-generated from Google Sheet: https://docs.google.com/spreadsheets/d/1ohiL6xOBbjC7La2iUdkjrVjG4IEUnVWhI0fRoarD6P0/edit?gid=1507296519#gid=1507296519
"""

# Domain → Topics → System Prompts mapping
DOMAIN_PROMPTS = '''
    
    # Convert dict to Python code
    code += "{\n"
    for domain, topics in domain_prompts.items():
        code += f'    "{domain}": {{\n'
        for topic, prompt in topics.items():
            # Escape quotes in prompt
            escaped_prompt = prompt.replace('"', '\\"').replace('\n', '\\n')
            code += f'        "{topic}": "{escaped_prompt}",\n'
        code += '    },\n'
    code += "}\n\n"
    
    # Add helper functions
    code += '''
def get_all_domains():
    """Get list of all domain names"""
    return list(DOMAIN_PROMPTS.keys())


def get_topics_for_domain(domain):
    """Get list of topics for a specific domain"""
    return list(DOMAIN_PROMPTS.get(domain, {}).keys())


def get_system_prompt(domain, topic):
    """Get system prompt for a specific domain and topic"""
    return DOMAIN_PROMPTS.get(domain, {}).get(topic, "")


def get_all_prompts():
    """Get all domain-topic-prompt combinations"""
    result = []
    for domain, topics in DOMAIN_PROMPTS.items():
        for topic, prompt in topics.items():
            result.append({
                "domain": domain,
                "topic": topic,
                "system_prompt": prompt
            })
    return result
'''
    
    # Write to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"✅ Generated: {file_path}")
    return True

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("EXTRACTING DOMAIN/TOPIC DATA FROM GOOGLE SHEET")
    print("=" * 80 + "\n")
    
    # Extract data
    domain_prompts = extract_from_google_sheet()
    
    if domain_prompts:
        print("\n" + "=" * 80)
        print("GENERATING PYTHON FILE WITH HARDCODED DATA")
        print("=" * 80)
        
        if generate_domain_prompts_file(domain_prompts):
            print("\n" + "=" * 80)
            print("✅ SUCCESS - Domain prompts extracted and hardcoded!")
            print("=" * 80)
            print("\nNext steps:")
            print("  1. Review: services/domain_prompts.py")
            print("  2. Run app: python -B main_image2video.py")
            print("  3. Test: Select domain → topics should match your Sheet")
        else:
            print("\n❌ Failed to generate file")
    else:
        print("\n" + "=" * 80)
        print("❌ FAILED TO EXTRACT DATA")
        print("=" * 80)
        print("\nManual steps:")
        print("  1. Go to: https://docs.google.com/spreadsheets/d/1ohiL6xOBbjC7La2iUdkjrVjG4IEUnVWhI0fRoarD6P0/edit")
        print("  2. File → Share → Publish to web")
        print("  3. Select sheet and 'Comma-separated values (.csv)'")
        print("  4. Copy published URL and update script")
        print("\nOr provide the sheet data in another format")