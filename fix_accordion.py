# -*- coding: utf-8 -*-
"""Fix: Restore GroupBox content that disappeared"""

import os
import shutil

def restore_groupbox_content():
    """Remove problematic stylesheet and use proper margins only"""
    
    file_path = os.path.join("ui", "text2video_panel.py")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup
    backup = file_path + '.backup_before_restore'
    shutil.copy2(file_path, backup)
    print(f"✅ Backup: {backup}")
    
    # Fix 1: Remove the problematic stylesheet that's hiding content
    old_apply_styles = '''    def _apply_styles(self):
        # Fix QGroupBox title visibility
        self.setStyleSheet("""
        QGroupBox {
            font-weight: bold;
            font-size: 13px;
            border: 1px solid #d0d0d0;
            border-radius: 5px;
            margin-top: 18px;
            padding-top: 18px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 4px 10px;
            left: 10px;
        }
        """)'''
    
    new_apply_styles = '''    def _apply_styles(self):
        # Unified theme v2 handles all styling
        pass'''
    
    if old_apply_styles in content:
        content = content.replace(old_apply_styles, new_apply_styles)
        print("✅ Removed problematic stylesheet")
    
    # Fix 2: Ensure proper margins (keep existing good values)
    # These should already be set to (10, 20, 10, 10) from previous fix
    
    # Fix 3: Add explicit QGroupBox styling that doesn't break children
    # Find the _build_ui method end and add stylesheet to specific groups
    
    # Add individual stylesheets to each GroupBox
    voice_group_pattern = '        colL.addWidget(voice_group)'
    if voice_group_pattern in content:
        new_voice = '''        voice_group.setStyleSheet("QGroupBox { font-weight: bold; margin-top: 10px; padding-top: 15px; }")
        colL.addWidget(voice_group)'''
        content = content.replace(voice_group_pattern, new_voice)
        print("✅ Added Voice Settings styling")
    
    domain_group_pattern = '        colL.addWidget(domain_group)'
    if domain_group_pattern in content:
        new_domain = '''        domain_group.setStyleSheet("QGroupBox { font-weight: bold; margin-top: 10px; padding-top: 15px; }")
        colL.addWidget(domain_group)'''
        content = content.replace(domain_group_pattern, new_domain)
        print("✅ Added Domain styling")
    
    download_group_pattern = '        colL.addWidget(download_group)'
    if download_group_pattern in content:
        new_download = '''        download_group.setStyleSheet("QGroupBox { font-weight: bold; margin-top: 10px; padding-top: 15px; }")
        colL.addWidget(download_group)'''
        content = content.replace(download_group_pattern, new_download)
        print("✅ Added Download styling")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Restored content visibility")
    return True

if __name__ == "__main__":
    print("🚑 Restoring GroupBox content visibility...\n")
    
    if restore_groupbox_content():
        print("\n🎉 Content should be visible now!")
        print("\nRestart app:")
        print("  python -B main_image2video.py")
    else:
        print("\n❌ Failed to restore")