# -*- coding: utf-8 -*-
"""
Voice Options for Text-to-Speech
Supports Google TTS and ElevenLabs providers
"""

from typing import Dict, List, Tuple

# Google TTS Voices Configuration
GOOGLE_TTS_VOICES = {
    "vi": [
        ("vi-VN-Standard-A", "🇻🇳 Nam Miền Bắc (Standard)"),
        ("vi-VN-Standard-B", "🇻🇳 Nữ Miền Nam (Standard)"),
        ("vi-VN-Wavenet-A", "🇻🇳 Nam Wavenet (Premium)"),
        ("vi-VN-Wavenet-B", "🇻🇳 Nữ Wavenet (Premium)"),
    ],
    "en": [
        ("en-US-Neural2-A", "🇺🇸 Male (Neural)"),
        ("en-US-Neural2-C", "🇺🇸 Female (Neural)"),
        ("en-GB-Neural2-A", "🇬🇧 Male British (Neural)"),
        ("en-GB-Neural2-B", "🇬🇧 Female British (Neural)"),
    ],
    "ja": [
        ("ja-JP-Neural2-B", "🇯🇵 Male (Neural)"),
        ("ja-JP-Neural2-C", "🇯🇵 Female (Neural)"),
    ],
    "ko": [
        ("ko-KR-Neural2-A", "🇰🇷 Male (Neural)"),
        ("ko-KR-Neural2-B", "🇰🇷 Female (Neural)"),
    ],
    "zh": [
        ("zh-CN-Standard-A", "🇨🇳 Female (Standard)"),
        ("zh-CN-Standard-B", "🇨🇳 Male (Standard)"),
    ],
}

# ElevenLabs Voices Configuration
ELEVENLABS_VOICES = [
    ("adam", "Adam (Deep & Authoritative)"),
    ("rachel", "Rachel (Calm Narration)"),
    ("antoni", "Antoni (Young & Energetic)"),
    ("bella", "Bella (Soft & Friendly)"),
    ("elli", "Elli (Warm & Professional)"),
    ("josh", "Josh (Natural & Conversational)"),
]

# TTS Providers
TTS_PROVIDERS = [
    ("google", "Google TTS"),
    ("elevenlabs", "ElevenLabs"),
]


def get_voices_for_provider(provider: str, language_code: str = "vi") -> List[Tuple[str, str]]:
    """
    Get available voices for a TTS provider
    
    Args:
        provider: "google" or "elevenlabs"
        language_code: Language code (for Google TTS only)
    
    Returns:
        List of (voice_id, display_name) tuples
    """
    if provider == "google":
        return GOOGLE_TTS_VOICES.get(language_code, GOOGLE_TTS_VOICES["vi"])
    elif provider == "elevenlabs":
        return ELEVENLABS_VOICES
    else:
        return []


def get_default_voice(provider: str, language_code: str = "vi") -> str:
    """
    Get default voice ID for a provider and language
    
    Args:
        provider: "google" or "elevenlabs"
        language_code: Language code (for Google TTS only)
    
    Returns:
        Default voice ID
    """
    voices = get_voices_for_provider(provider, language_code)
    return voices[0][0] if voices else ""


def get_voice_config(provider: str, voice_id: str, language_code: str = "vi") -> Dict:
    """
    Get voice configuration for script generation
    
    Args:
        provider: "google" or "elevenlabs"
        voice_id: Voice ID
        language_code: Language code
    
    Returns:
        Dict with voice configuration
    """
    return {
        "provider": provider,
        "voice_id": voice_id,
        "language_code": language_code,
    }
