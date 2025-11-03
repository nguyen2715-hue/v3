# -*- coding: utf-8 -*-
"""Remove all txt_prompt_preview references from text2video_panel.py"""

import os
import shutil

def fix_preview_references():
    file_path = os.path.join("ui", "text2video_panel.py")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Backup
    backup = file_path + '.backup_remove_preview'
    shutil.copy2(file_path, backup)
    print(f"✅ Backup: {backup}\n")
    
    fixed_lines = []
    changes = 0
    
    for i, line in enumerate(lines):
        # Skip lines with txt_prompt_preview
        if 'txt_prompt_preview' in line:
            print(f"❌ Line {i+1}: {line.strip()}")
            
            # If it's .clear(), just comment it out
            if '.clear()' in line:
                indent = len(line) - len(line.lstrip())
                fixed_lines.append(' ' * indent + '# Preview removed\n')
                changes += 1
                print(f"   → Commented out")
            
            # If it's .setPlainText(), replace with log
            elif '.setPlainText(' in line:
                indent = len(line) - len(line.lstrip())
                # Extract the content being set
                if 'preview' in line:
                    fixed_lines.append(' ' * indent + '# Preview removed - content not displayed\n')
                else:
                    fixed_lines.append(' ' * indent + 'pass  # Preview removed\n')
                changes += 1
                print(f"   → Replaced with pass")
            else:
                # Skip other preview-related lines
                changes += 1
                print(f"   → Skipped")
        else:
            fixed_lines.append(line)
    
    if changes > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print(f"\n✅ Fixed {changes} references to txt_prompt_preview")
        return True
    else:
        print("\n✅ No references found (already fixed?)")
        return False

if __name__ == "__main__":
    print("🔧 Removing txt_prompt_preview references...\n")
    
    if fix_preview_references():
        print("\n✅ Done! Run app:")
        print("  python -B main_image2video.py")
    else:
        print("\nMay already be fixed, or manual intervention needed")