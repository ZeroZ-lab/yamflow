from typing import Any, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class Context:
    """工作流上下文管理"""
    variables: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def set(self, key: str, value: Any) -> None:
        """设置上下文变量"""
        self.variables[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取上下文变量"""
        return self.variables.get(key, default)
    
    def update(self, data: Dict[str, Any]) -> None:
        """批量更新上下文变量"""
        self.variables.update(data)
    
    def clear(self) -> None:
        """清除所有上下文变量"""
        self.variables.clear() 