import pytest
from src.core.engine import WorkflowEngine
from src.core.errors import (
    WorkflowValidationError,
    WorkflowExecutionError,
    NodeNotFoundError
)

async def test_workflow_engine_initialization(sample_workflow_config):
    """测试工作流引擎初始化"""
    engine = WorkflowEngine(sample_workflow_config)
    assert engine.config == sample_workflow_config
    assert engine.nodes == {}
    assert engine.context is not None

async def test_workflow_load_and_validate(sample_workflow_config):
    """测试工作流配置加载和验证"""
    engine = WorkflowEngine(sample_workflow_config)
    await engine.load()
    
    # 验证节点是否正确加载
    assert "input" in engine.nodes
    assert "ai_processor" in engine.nodes
    assert "output" in engine.nodes

async def test_workflow_execution(sample_workflow_config):
    """测试工作流执行"""
    engine = WorkflowEngine(sample_workflow_config)
    await engine.load()
    
    input_data = "What is Python?"
    result = await engine.execute(input_data)
    
    assert result is not None
    assert isinstance(result, dict)
    assert "output" in result

async def test_invalid_workflow_config():
    """测试无效的工作流配置"""
    invalid_config = {
        "version": "1.0",
        "name": "Invalid Workflow",
        "nodes": []  # 缺少必要的节点
    }
    
    engine = WorkflowEngine(invalid_config)
    with pytest.raises(WorkflowValidationError):
        await engine.load()

async def test_workflow_edge_building():
    """测试边的构建"""
    config = {
        "version": "1.0",
        "name": "Test Workflow",
        "nodes": [
            {"id": "node1", "type": "f.input"},
            {"id": "node2", "type": "f.output"}
        ],
        "edges": [
            {"source": "node1", "target": "node2", "type": "main"}
        ]
    }
    
    engine = WorkflowEngine(config)
    await engine.load()
    
    assert "node1" in engine.edges
    assert engine.edges["node1"] == ["node2"]

async def test_node_not_found_error():
    """测试节点未找到错误"""
    config = {
        "version": "1.0",
        "name": "Test Workflow",
        "nodes": [
            {"id": "input", "type": "f.input"}
        ],
        "edges": [
            {"source": "input", "target": "non_existent", "type": "main"}
        ]
    }
    
    engine = WorkflowEngine(config)
    await engine.load()
    
    with pytest.raises(NodeNotFoundError):
        await engine.execute("test input")