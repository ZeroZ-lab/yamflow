import pytest
from core.context import Context

def test_context_initialization():
    """测试上下文初始化"""
    context = Context()
    assert context.variables == {}
    assert context.metadata == {}

def test_context_set_get():
    """测试上下文变量的设置和获取"""
    context = Context()
    
    # 测试设置和获取单个值
    context.set("key1", "value1")
    assert context.get("key1") == "value1"
    
    # 测试获取默认值
    assert context.get("non_existent", "default") == "default"
    
    # 测试获取不存在的键
    assert context.get("non_existent") is None

def test_context_update():
    """测试上下文批量更新"""
    context = Context()
    
    # 测试批量更新
    update_data = {
        "key1": "value1",
        "key2": "value2"
    }
    context.update(update_data)
    
    assert context.get("key1") == "value1"
    assert context.get("key2") == "value2"

def test_context_clear():
    """测试上下文清除"""
    context = Context()
    
    # 设置一些数据
    context.set("key1", "value1")
    context.set("key2", "value2")
    
    # 清除数据
    context.clear()
    
    assert context.variables == {}
    assert context.get("key1") is None
    assert context.get("key2") is None 