import pytest
import torch
import onnx
import numpy as np

from trolo.export import ModelExporter
from trolo.utils.smart_defaults import infer_pretrained_model

DEFAULT_MODEL = "dfine_n.pth"

@pytest.fixture(scope="session")
def model_path():
    return infer_pretrained_model(DEFAULT_MODEL)

@pytest.fixture
def exporter(model_path):
    return ModelExporter(DEFAULT_MODEL)

def test_onnx_export(exporter, tmp_path):
    input_size = (640, 640)
    default_dynamic_axes = {'images': {0: 'N'}, 'orig_target_sizes': {0: 'N'}}
    
    # formatted_data = format_input(input_data)
    
    exporter.export(
        export_format='onnx', 
        input_size=input_size
    )

@pytest.mark.parametrize("input_size", [
    (640, 640)
])
def test_export_variable_input_sizes(exporter, input_size):
    default_dynamic_axes = {'images': {0: 'N'}, 'orig_target_sizes': {0: 'N'}}
    
    exporter.export(
        export_format='onnx', 
        input_size=input_size       
    )

def test_export_with_custom_dynamic_axes(exporter):
    input_size = (640, 640)
    custom_dynamic_axes = {
        'images': {0: 'batch', 2: 'height', 3: 'width'},
        'orig_target_sizes': {0: 'batch'}
    }
    
    exporter.export(
        export_format='onnx', 
        input_size=input_size
    )

def test_export_with_simplification(exporter):
    input_size = (640, 640)
    default_dynamic_axes = {'images': {0: 'N'}, 'orig_target_sizes': {0: 'N'}}
    
    exporter.export(
        export_format='onnx', 
        input_size=input_size
    )

def test_export_invalid_format(exporter):
    input_size = (640, 640)
    default_dynamic_axes = {'images': {0: 'N'}, 'orig_target_sizes': {0: 'N'}}
    
    with pytest.raises(ValueError, match="Export format is missing!"):
        exporter.export(
            export_format=None, 
            input_size=input_size            
        )
