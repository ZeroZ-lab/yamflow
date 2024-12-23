import pytest
from src.core.context import Context

def test_context_initialization():
    """测试上下文初始化"""
    context = Context()
    assert context.variables == {}
    assert context.metadata == {}

def test_context_set_get():
    """测试上下文变量的设置和获取"""
    context = Context()
    context.set("key1", "value1")
    assert context.get("key1") == "value1"
    assert context.get("non_existent", "default") == "default"
    assert context.get("non_existent") is None

def test_context_update():
    """测试上下文批量更新"""
    context = Context()
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
    context.set("key1", "value1")
    context.set("key2", "value2")
    context.clear()
    assert context.variables == {}
    assert context.get("key1") is None
    assert context.get("key2") is None