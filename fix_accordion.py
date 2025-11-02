#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix 2 issues:
1. Reduce spacer: 20px → 10px (labels too far right)
2. Fix image generation API call (wrong parameter name)
"""
import shutil
from datetime import datetime

def main():
    file_path = r"ui\video_ban_hang_panel.py"
    
    print("="*70)
    print(" FIX SPACING + IMAGE API ".center(70, "="))
    print("="*70)
    print("\n📋 Fixes:")
    print("  1. Spacer: 20px → 10px (bring right labels closer)")
    print("  2. Fix image API call (wrong parameter)")
    print("="*70)
    
    response = input("\n🚀 Apply? (y/n): ")
    if response.lower() != 'y':
        return
    
    # Backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    shutil.copy2(file_path, backup_path)
    print(f"\n✓ Backup: {backup_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # ====================================================================
    # FIX 1: Reduce spacer column (20px → 10px)
    # ====================================================================
    
    spacer_patterns = [
        ('form.setColumnMinimumWidth(2, 20)', 'form.setColumnMinimumWidth(2, 10)'),
        ('setColumnMinimumWidth(2, 20)', 'setColumnMinimumWidth(2, 10)'),
    ]
    
    for old, new in spacer_patterns:
        if old in content:
            content = content.replace(old, new)
            changes.append("✓ Fix 1: Spacer 20px → 10px")
            break
    
    # ====================================================================
    # FIX 2: Fix image generation API call
    # Change: generate_image_with_rate_limit(prompt=...) 
    # To: generate_image_with_rate_limit(text=...)
    # ====================================================================
    
    # Pattern 1: Scene images
    old_api_call = '''                        img_data_url = image_gen_service.generate_image_with_rate_limit(
                            prompt=prompt,
                            api_keys=api_keys,
                            model=model,
                            aspect_ratio=aspect_ratio,
                            delay_before=0,  # Explicitly no extra delay
                            logger=lambda msg: self.progress.emit(msg),
                        )'''
    
    new_api_call = '''                        img_data_url = image_gen_service.generate_image_with_rate_limit(
                            text=prompt,  # Fixed: 'prompt' → 'text'
                            api_keys=api_keys,
                            model=model,
                            aspect_ratio=aspect_ratio,
                            delay_before=0,
                            logger=lambda msg: self.progress.emit(msg),
                        )'''
    
    if old_api_call in content:
        content = content.replace(old_api_call, new_api_call)
        changes.append("✓ Fix 2a: Fixed scene image API call")
    
    # Pattern 2: Thumbnails
    old_thumb_call = '''                    thumb_data_url = image_gen_service.generate_image_with_rate_limit(
                        prompt=prompt,
                        api_keys=api_keys,
                        model=model,
                        aspect_ratio=aspect_ratio,
                        delay_before=0,
                        logger=lambda msg: self.progress.emit(msg)
                    )'''
    
    new_thumb_call = '''                    thumb_data_url = image_gen_service.generate_image_with_rate_limit(
                        text=prompt,  # Fixed: 'prompt' → 'text'
                        api_keys=api_keys,
                        model=model,
                        aspect_ratio=aspect_ratio,
                        delay_before=0,
                        logger=lambda msg: self.progress.emit(msg)
                    )'''
    
    if old_thumb_call in content:
        content = content.replace(old_thumb_call, new_thumb_call)
        changes.append("✓ Fix 2b: Fixed thumbnail API call")
    
    if not changes:
        print("\n⚠ No changes - patterns not found")
        print("\nSearching for current state...")
        
        # Debug: Show current spacer setting
        if 'setColumnMinimumWidth(2,' in content:
            import re
            match = re.search(r'setColumnMinimumWidth\(2,\s*(\d+)\)', content)
            if match:
                print(f"  Current spacer: {match.group(1)}px")
        
        # Debug: Show current API call
        if 'generate_image_with_rate_limit(' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'generate_image_with_rate_limit(' in line:
                    print(f"\n  Line {i+1}: {line.strip()}")
                    if i+1 < len(lines):
                        print(f"  Line {i+2}: {lines[i+1].strip()}")
                    break
        
        return False
    
    # Write
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n" + "="*70)
    print("✓ BOTH ISSUES FIXED!")
    print("="*70)
    for change in changes:
        print(change)
    
    print(f"\n💾 Backup: {backup_path}")
    print("\n🧪 Test:")
    print("  1. py -B main_image2video.py")
    print("  2. Check right labels position")
    print("  3. Try 'Viết kịch bản' + 'Tạo ảnh'")
    
    return True

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()