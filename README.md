# AWF (AI Workflow Framework)

AWF is a lightweight AI workflow framework that defines and executes AI processing flows through YAML configuration files. It supports multiple LLM providers and can be easily extended with new processing nodes.

## ✨ Features

- 📝 YAML-based graph structure configuration
- 🔄 Support for complex workflow orchestration
- 🧩 Modular node system
- 🔌 Easily extensible LLM provider support
- 🛠️ Command-line tools
- 🎯 Powerful context management
- 🎨 Visual editing support

## 🚀 Quick Start

### Installation

```bash
pip install awf
```

### Create a Workflow

Create a `workflow.yaml` file:

```yaml
version: "1.0"
name: "OpenRouter AI Flow"

metadata:
  description: "OpenRouter AI Workflow"
  author: "AWF Team"
  tags: ["ai", "openrouter"]

nodes:
  - id: "input"
    type: "f.input"
    
  - id: "ai_processor"
    type: "ai.generate"
    config:
      provider: "openrouter"
      model: "anthropic/claude-3-opus"
      parameters:
        temperature: 0.7
        max_tokens: 4096
        route_prefix: "experimental"
        transforms: ["streaming"]
        
  - id: "output"
    type: "f.output"

edges:
  - source: "input"
    target: "ai_processor"
    type: "main"
    
  - source: "ai_processor"
    target: "output"
    type: "main"

ui_metadata:
  theme: "light"
  layout: "horizontal"
  zoom: 1.0
  pan: [0, 0]
```

### Run the Workflow

```bash
awf --f workflow.yaml --input "What is the time complexity of quicksort?"
```

## 📦 Node Type System

AWF uses a clean prefix naming system to distinguish different types of nodes:

### Flow Control Nodes (f.*)
Built-in framework nodes responsible for workflow control without specific business logic.

#### Basic Nodes
- `f.input` - Input node, workflow starting point
- `f.output` - Output node, workflow endpoint
- `f.noop` - No-operation node for placeholding or debugging

#### Conditional Control
- `f.if` - Conditional node supporting if-else branches
- `f.switch` - Multi-path branching based on conditions
- `f.match` - Pattern matching node with complex matching support

#### Loop Control
- `f.loop` - Basic loop node with while/until conditions
- `f.foreach` - Iteration node for array/list processing
- `f.repeat` - Repeat execution node for specified iterations

#### Concurrent Control
- `f.parallel` - Parallel execution node
- `f.race` - Race execution node, uses first completed result
- `f.merge` - Merge node for combining multiple branch results

Example:
```yaml
nodes:
  - id: "parallel_process"
    type: "f.parallel"
    config:
      branches: ["security", "quality", "performance"]
      join: "all"  # Wait for all branches to complete
      
  - id: "error_handler"
    type: "f.try"
    config:
      catch: ["ApiError", "TimeoutError"]
      retry: 3
      fallback: "backup_process"
```

### AI Processing Nodes (ai.*)
Contains specific AI business logic with provider and model configurations.

- `ai.classify` - Classification node
- `ai.extract` - Parameter extraction node
- `ai.generate` - Content generation node
- `ai.summarize` - Summary generation node

Example:
```yaml
- id: "classifier"
  type: "ai.classify"
  provider: "openai"    # AI provider
  model: "gpt-4"       # Model configuration
  config:              # Business configuration
    categories: ["coding", "general", "math"]
```

### Utility Nodes (util.*)
Utility nodes provide general data processing and auxiliary functions.

- `util.transform` - Data transformation node
- `util.validate` - Data validation node
- `util.log` - Logging node

### Complete Example

```yaml
version: "1.0"
name: "Question Answering Flow"

metadata:
  description: "AI Question Answering Workflow"
  author: "AWF Team"
  tags: ["qa", "ai"]

nodes:
  - id: "input"
    type: "f.input"
    
  - id: "classifier"
    type: "ai.classify"
    config:
      provider: "openai"
      model: "gpt-4"
      parameters:
        categories: ["coding", "general", "math"]
    
  - id: "extractor"
    type: "type.ai.extractor"
    config:
      provider: "anthropic"
      model: "claude-3"
      parameters:
        - name: "language"
          type: "string"
        - name: "complexity"
          type: "enum"
          values: ["simple", "medium", "complex"]
          
  - id: "output"
    type: "type.flow.output"

edges:
  - source: "input"
    target: "classifier"
    type: "main"
    
  - source: "classifier"
    target: "extractor"
    type: "main"
    conditions:
      - when: "context.category == 'coding'"
        config:
          retry: 3
          timeout: 30
          
  - source: "extractor"
    target: "output"
    type: "main"
```

## 🔧 Configuration

### Environment Variables
AWF supports loading environment variables through `.env` files. Create a `.env` file in your project root:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1  # 可选
```

Run with custom environment files:
```bash
# Use default .env file
awf --f workflow.yaml --input "Your question"

# Use custom env file
awf --f workflow.yaml --env /path/to/custom.env --input "Your question"
```

### Provider Configuration
```yaml
# config.yaml
providers:
  openai:
    api_key: ${OPENAI_API_KEY}
    default_model: "gpt-4"
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    default_model: "claude-3"
  openrouter:
    api_key: ${OPENROUTER_API_KEY}
    default_model: "anthropic/claude-3-opus"
    base_url: "https://openrouter.ai/api/v1"
    models:
      - "anthropic/claude-3-opus"
      - "anthropic/claude-3-sonnet"
      - "google/gemini-pro"
      - "meta/llama-3"
      - "mistral/mistral-large"
      - "openai/gpt-4-turbo"
```

### Workflow Configuration Structure

```yaml
version: "1.0"        # Version number
name: "Workflow Name" # Workflow name

metadata:             # Metadata
  description: "..."  # Description
  author: "..."      # Author
  tags: []           # Tags

nodes:               # Node definitions
  - id: "node_id"    # Node ID
    type: "..."      # Node type
    config: {}       # Node configuration

edges:               # Edge definitions
  - source: "..."    # Source node
    target: "..."    # Target node
    type: "..."      # Edge type
    conditions: []   # Conditions
```

## 🎯 Examples

More examples can be found in the `examples/` directory:

- Basic Q&A workflow
- Conditional branching workflow
- Parallel processing workflow
- Complex graph structure workflow

## 📖 Documentation

For detailed documentation, visit: [AWF Documentation](https://awf.readthedocs.io/)

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. Update tests
2. Update documentation
3. Follow code style guidelines

## 📄 License

MIT License

## 🙏 Acknowledgments

Thanks to all contributors!