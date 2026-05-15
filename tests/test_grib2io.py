import os

import pytest
import ujson

from kerchunk.grib2 import scan_grib

pytest.importorskip("grib2io")
pytest.importorskip("cfgrib")

HERE = os.path.dirname(__file__)


def _scan_with_engine(monkeypatch, engine, path):
    monkeypatch.setenv("KERCHUNK_GRIB_ENGINE", engine)
    return scan_grib(path)


def _data_var_names(message_group):
    refs = message_group["refs"]
    attrs = ujson.loads(refs[".zattrs"])
    coordinates = set(attrs.get("coordinates", "").split())
    names = set()
    for key in refs:
        name = key.split("/")[0]
        if name in {".zattrs", ".zgroup"}:
            continue
        if name in coordinates:
            continue
        names.add(name)
    return names


@pytest.mark.parametrize(
    "file_name, expected_count",
    [
        ("tinygrib.grb2", 1),
        ("hrrr.wrfsubhf.sample.grib2", 2),
    ],
)
def test_grib2io_scan_counts_match_cfgrib(monkeypatch, file_name, expected_count):
    path = os.path.join(HERE, file_name)

    cfgrib_out = _scan_with_engine(monkeypatch, "cfgrib", path)
    grib2io_out = _scan_with_engine(monkeypatch, "grib2io", path)

    assert len(cfgrib_out) == expected_count
    assert len(grib2io_out) == expected_count


@pytest.mark.parametrize("file_name", ["tinygrib.grb2", "hrrr.wrfsubhf.sample.grib2"])
def test_grib2io_scan_output_schema(monkeypatch, file_name):
    path = os.path.join(HERE, file_name)
    out = _scan_with_engine(monkeypatch, "grib2io", path)

    assert out
    for message_group in out:
        assert message_group["version"] == 1
        assert "refs" in message_group
        assert "templates" in message_group
        assert message_group["templates"]["u"] == path
        assert ".zattrs" in message_group["refs"]
        assert ".zgroup" in message_group["refs"]


@pytest.mark.parametrize("file_name", ["tinygrib.grb2", "hrrr.wrfsubhf.sample.grib2"])
def test_grib2io_scan_has_data_var_per_message(monkeypatch, file_name):
    path = os.path.join(HERE, file_name)
    out = _scan_with_engine(monkeypatch, "grib2io", path)

    for message_group in out:
        names = _data_var_names(message_group)
        assert len(names) == 1
