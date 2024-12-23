from typing import Optional

class WorkflowError(Exception):
    """工作流基础异常类"""
    def __init__(self, message: str, details: Optional[dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)

class WorkflowValidationError(WorkflowError):
    """工作流验证错误"""
    pass

class WorkflowExecutionError(WorkflowError):
    """工作流执行错误"""
    pass

class NodeNotFoundError(WorkflowError):
    """节点未找到错误"""
    pass 