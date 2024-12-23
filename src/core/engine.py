from typing import Any, Dict, List, Optional
import asyncio
from pydantic import BaseModel, ValidationError

from .errors import (
    WorkflowValidationError,
    WorkflowExecutionError,
    NodeNotFoundError
)
from .context import Context

async def create_node(node_id: str, node_type: str, config: dict):
    """临时的 mock 节点创建函数"""
    class MockNode:
        def __init__(self, id: str, type: str, config: dict):
            self.id = id
            self.type = type
            self.config = config
            
        async def execute(self, context):
            return "mock result"
    
    return MockNode(node_id, node_type, config)

class WorkflowConfig(BaseModel):
    """工作流配置验证模型"""
    version: str
    name: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None

class WorkflowEngine:
    """工作流引擎核心类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.nodes = {}  # 存储节点实例
        self.edges = {}  # 存储边的连接关系
        self.context = Context()
        self._validated = False
    
    async def load(self) -> None:
        """加载并验证工作流配置"""
        try:
            # 验证配置结构
            workflow_config = WorkflowConfig(**self.config)
            
            # 构建边的连接关系
            self.edges = self._build_edges(workflow_config.edges)
            
            # 实例化节点
            await self._instantiate_nodes(workflow_config.nodes)
            
            self._validated = True
            
        except ValidationError as e:
            raise WorkflowValidationError("Invalid workflow configuration", 
                                        details={"errors": e.errors()})
        except Exception as e:
            raise WorkflowValidationError(str(e))
    
    async def execute(self, input_data: Any) -> Dict[str, Any]:
        """执行工作流"""
        if not self._validated:
            await self.load()
        
        try:
            # 设置输入数据到上下文
            self.context.set("input", input_data)
            
            # 从入口节点开始执行
            entry_node = self._find_entry_node()
            result = await self._execute_node(entry_node)
            
            return {"output": result}
            
        except Exception as e:
            raise WorkflowExecutionError(f"Workflow execution failed: {str(e)}")
    
    async def _execute_node(self, node_id: str) -> Any:
        """执行单个节点"""
        if node_id not in self.nodes:
            raise NodeNotFoundError(f"Node not found: {node_id}")
        
        node = self.nodes[node_id]
        
        try:
            # 执行节点
            result = await node.execute(self.context)
            
            # 获取下一个节点
            next_nodes = self.edges.get(node_id, [])
            
            if not next_nodes:
                return result
            
            # 执行后续节点
            tasks = [self._execute_node(next_node) for next_node in next_nodes]
            results = await asyncio.gather(*tasks)
            
            return results[0] if len(results) == 1 else results
            
        except Exception as e:
            raise WorkflowExecutionError(
                f"Error executing node {node_id}: {str(e)}"
            )
    
    def _build_edges(self, edges: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """构建边的连接关系"""
        edge_map = {}
        for edge in edges:
            source = edge["source"]
            target = edge["target"]
            if source not in edge_map:
                edge_map[source] = []
            edge_map[source].append(target)
        return edge_map
    
    async def _instantiate_nodes(self, nodes: List[Dict[str, Any]]) -> None:
        """实例化所有节点"""
        for node_config in nodes:
            node_id = node_config["id"]
            node_type = node_config["type"]
            node_instance = await create_node(
                node_id,
                node_type,
                node_config.get("config", {})
            )
            self.nodes[node_id] = node_instance
    
    def _find_entry_node(self) -> str:
        """查找入口节点"""
        # 查找类型为 f.input 的节点
        for node_id, node in self.nodes.items():
            if node.type == "f.input":
                return node_id
        raise WorkflowValidationError("No entry node (f.input) found in workflow") 