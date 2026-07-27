from pathlib import Path

import main


def test_cleaned_text_is_saved_to_raw_text_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    output_path = main._save_text_file("benefits.txt", "  Hello   \n\nWorld  ")

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == "Hello\nWorld"
    assert output_path.parent == tmp_path / "raw_text"
