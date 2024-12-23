import pytest
from src.core.engine import WorkflowEngine
from src.core.errors import WorkflowValidationError

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

async def test_workflow_context_management(sample_workflow_config):
    """测试工作流上下文管理"""
    engine = WorkflowEngine(sample_workflow_config)
    await engine.load()
    
    # 设置上下文变量
    engine.context.set("test_var", "test_value")
    
    # 执行工作流
    result = await engine.execute("test input")
    
    # 验证上下文变量是否正确传递
    assert engine.context.get("test_var") == "test_value" 