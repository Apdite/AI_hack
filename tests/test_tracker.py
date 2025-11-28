import pytest
from models.video_tracker import analyze_video

def test_analyze():
    df = analyze_video('data/sample_video.mp4')  # Замените на короткий тест-видео
    assert not df.empty
    assert df['id'].nunique() > 0