import json
import subprocess
import sys

import pytest

from energy_lab.__main__ import PROJECT_ROOT, main


def test_default_cli_output(capsys):
    assert main([]) == 0
    output = capsys.readouterr().out
    assert "3.900 kWh" in output
    assert "3.12 yuan" in output


def test_json_output_and_custom_price(capsys):
    assert main(["--json", "--price", "1.0"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["total_cost"] == 3.9


def test_custom_file_from_temporary_directory(tmp_path, capsys):
    path = tmp_path / "devices.json"
    path.write_text('[{"name": "test", "power_w": 500, "hours": 2}]', encoding="utf-8")
    assert main(["--data", str(path), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["total_kwh"] == 1


def test_default_data_is_independent_of_working_directory(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["--json"]) == 0
    assert json.loads(capsys.readouterr().out)["total_cost"] == 3.12


def test_missing_input_has_clear_error(tmp_path, capsys):
    with pytest.raises(SystemExit) as error:
        main(["--data", str(tmp_path / "missing.json")])
    assert error.value.code == 2
    assert "Input error:" in capsys.readouterr().err


def test_broken_json_has_clear_error(tmp_path, capsys):
    path = tmp_path / "broken.json"
    path.write_text("not JSON", encoding="utf-8")
    with pytest.raises(SystemExit) as error:
        main(["--data", str(path)])
    assert error.value.code == 2
    assert "Input error:" in capsys.readouterr().err


def test_negative_hours_has_clear_error(capsys):
    with pytest.raises(SystemExit) as error:
        main(["--data", str(PROJECT_ROOT / "data" / "invalid_devices.json")])
    assert error.value.code == 2
    assert "hours" in capsys.readouterr().err


def test_script_entrypoint_from_another_directory(tmp_path):
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "main.py"), "--json"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["total_cost"] == 3.12
