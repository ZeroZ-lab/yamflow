import pytest
from pathlib import Path
import yaml

@pytest.fixture
def sample_workflow_config():
    """提供示例工作流配置"""
    return {
        "version": "1.0",
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "input",
                "type": "f.input"
            },
            {
                "id": "ai_processor",
                "type": "ai.generate",
                "config": {
                    "provider": "mock",  # 使用 mock provider 进行测试
                    "model": "test-model"
                }
            },
            {
                "id": "output",
                "type": "f.output"
            }
        ],
        "edges": [
            {
                "source": "input",
                "target": "ai_processor",
                "type": "main"
            },
            {
                "source": "ai_processor",
                "target": "output",
                "type": "main"
            }
        ]
    }

@pytest.fixture
def sample_workflow_file(tmp_path, sample_workflow_config):
    workflow_file = tmp_path / "workflow.yaml"
    with workflow_file.open("w") as f:
        yaml.dump(sample_workflow_config, f)
    return workflow_file 

@pytest.fixture
def sample_context():
    from core.context import Context
    return Context()

@pytest.fixture
def mock_node():
    """提供 mock 节点实现"""
    class MockNode:
        def __init__(self, node_id: str, node_type: str, config: dict):
            self.id = node_id
            self.type = node_type
            self.config = config

        async def execute(self, context):
            return "mock result"

    return MockNode