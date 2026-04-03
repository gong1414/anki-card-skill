import subprocess
import sys
import tempfile
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "anki_skill.cli", *args],
        capture_output=True,
        text=True,
    )


def test_cli_help():
    result = _run_cli("--help")
    assert result.returncode == 0
    assert "anki-export" in result.stdout or "usage" in result.stdout.lower()


def test_cli_tsv_export():
    input_file = FIXTURES / "sample_cards.txt"
    with tempfile.NamedTemporaryFile(suffix=".tsv", delete=False) as f:
        output = Path(f.name)
    result = _run_cli(str(input_file), "-f", "tsv", "-o", str(output))
    assert result.returncode == 0
    content = output.read_text(encoding="utf-8")
    assert len(content.splitlines()) == 3
    output.unlink()


def test_cli_apkg_export():
    input_file = FIXTURES / "sample_cards.txt"
    with tempfile.NamedTemporaryFile(suffix=".apkg", delete=False) as f:
        output = Path(f.name)
    result = _run_cli(
        str(input_file), "-f", "apkg", "-o", str(output), "-d", "Test"
    )
    assert result.returncode == 0
    assert output.stat().st_size > 0
    output.unlink()


def test_cli_stdin():
    """Support reading from stdin when input file is '-'."""
    with tempfile.NamedTemporaryFile(suffix=".tsv", delete=False) as f:
        output = Path(f.name)
    proc = subprocess.run(
        [sys.executable, "-m", "anki_skill.cli", "-", "-f", "tsv", "-o", str(output)],
        input="Q1 | A1 | tag1\n",
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    content = output.read_text(encoding="utf-8")
    assert "Q1" in content
    output.unlink()


def test_cli_missing_input():
    result = _run_cli()
    assert result.returncode != 0


def test_cli_file_not_found():
    result = _run_cli("/nonexistent/file.txt", "-f", "tsv", "-o", "/tmp/out.tsv")
    assert result.returncode == 1
    assert "not found" in result.stderr.lower()


def test_cli_empty_input_exits_nonzero():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
        f.write("")
        path = Path(f.name)
    result = _run_cli(str(path), "-f", "tsv", "-o", "/tmp/out.tsv")
    assert result.returncode == 2
    path.unlink()


def test_cli_output_dir_permission_denied(tmp_path):
    """CLI should exit gracefully when output directory is not writable."""
    input_file = FIXTURES / "sample_cards.txt"
    import platform
    if platform.system() == "Darwin":
        bad_output = "/private/var/audit/fakedir/out.tsv"
    else:
        bad_output = "/proc/fakedir/out.tsv"
    result = _run_cli(str(input_file), "-f", "tsv", "-o", bad_output)
    assert result.returncode == 3
    assert "error" in result.stderr.lower()
