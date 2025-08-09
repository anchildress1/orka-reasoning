# ChatMode System Documentation

## Overview

The ChatMode system in OrKa provides specialized, pre-configured AI workflows designed for specific use cases. The system implements domain-specific expertise and tooling to generate high-quality outputs for common tasks like architectural documentation, gap analysis, and system design.

## High-Level Big Picture Architect ChatMode

### Purpose

The `high-level-big-picture-architect` ChatMode specializes in explaining and documenting software systems at a high level for fast onboarding, architectural clarity, and gap discovery.

### Role Definition

- **Level**: Principal Systems Architect
- **Mission**: Explain and document software systems at a high level for fast onboarding, architectural clarity, and gap discovery

### Scope

The ChatMode focuses on:
- Interfaces, contracts, data flows
- Major components and their relationships
- Reliability behaviors and error surfaces
- Integration points and dependencies

## Inputs

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | The main request/question describing what to document |
| `targets` | string | Target components/systems to analyze |
| `artifactType` | enum | Type of artifact to generate |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `depth` | enum | `overview` | Level of detail (overview, subsystem, interface-only) |
| `constraints` | object | `{}` | Additional constraints for generation |

### Artifact Types

- **`doc`**: Generate comprehensive documentation
- **`diagram`**: Generate system diagrams
- **`testcases`**: Generate test case specifications
- **`gapscan`**: Generate gap analysis reports
- **`usecases`**: Generate use case documentation

### Depth Levels

- **`overview`**: High-level system overview
- **`subsystem`**: Detailed subsystem analysis
- **`interface-only`**: Focus only on interfaces and contracts

## Outputs

### Document Output
- **Type**: Markdown or Confluence format
- **Location**: `docs/` folder
- **Naming**: Timestamped filenames for traceability

### Diagram Output
- **Type**: Mermaid diagram files
- **Location**: `docs/diagrams/` folder
- **Formats**: Sequence, flowchart, class, ER, state diagrams

## Configuration Constraints

### Directory Structure
- **Preferred Docs Folder**: `docs/`
- **Diagram Folder**: `docs/diagrams/`
- **Diagram Engine**: Mermaid (enforced)
- **Default Format**: Markdown

### Footer Requirements
All generated documents include a footer:
```
_Generated with GitHub Copilot as directed by {USER_NAME}_
```

### Behaviors
- **Ask If Missing**: Prompts for missing required information
- **Highlight Gaps**: Identifies and emphasizes missing components
- **No Guessing**: Explicit about uncertainty rather than making assumptions
- **Iteration Until Complete**: Continues refinement until quality standards are met

## Usage

### CLI Usage

```bash
# Generate documentation
orka chatmode architect "Document the authentication system" "AuthService" \
  --artifact-type doc \
  --depth overview \
  --user-name "Your Name"

# Generate diagrams
orka chatmode architect "Show user registration flow" "UserService" \
  --artifact-type diagram \
  --diagram-type sequence \
  --depth subsystem

# Generate gap analysis
orka chatmode architect "Analyze testing coverage" "TestSuite" \
  --artifact-type gapscan \
  --depth overview

# Generate use cases
orka chatmode architect "Document user workflows" "UserInterface" \
  --artifact-type usecases \
  --depth interface-only
```

### Programmatic Usage

```python
from orka.agents.architectural_documentation_agent import ArchitecturalDocumentationAgent

# Create agent
agent = ArchitecturalDocumentationAgent(
    "architect-agent",
    workspace_path="."
)

await agent.initialize()

# Process request
context = {
    "prompt": "Document the payment processing system",
    "targets": "PaymentService",
    "artifactType": "doc",
    "depth": "overview",
    "user_name": "Developer"
}

result = await agent.process("Payment system documentation", context)
```

### YAML Configuration

```yaml
orchestrator:
  id: documentation-workflow
  strategy: sequential
  agents: [doc_generator]

agents:
  - id: doc_generator
    type: architectural-documentation
    prompt: "Generate documentation for: {{ input }}"
    params:
      artifact_type: "{{ artifact_type | default('doc') }}"
      targets: "{{ targets }}"
      depth: "{{ depth | default('overview') }}"
      user_name: "{{ user_name | default('User') }}"
```

## File Organization

### Generated Documents

Documents are automatically organized in the workspace:

```
docs/
├── architecture_doc_20250809_143022.md
├── testcases_20250809_143045.md
├── gapscan_20250809_143101.md
└── diagrams/
    ├── flowchart_20250809_143022.mmd
    ├── sequence_20250809_143045.mmd
    └── class_20250809_143101.mmd
```

### Naming Convention

- **Documents**: `{artifact_type}_{timestamp}.md`
- **Diagrams**: `{diagram_type}_{timestamp}.mmd`
- **Timestamp**: `YYYYMMDD_HHMMSS` format

## Supported Tools

The ChatMode integrates with various tools for comprehensive analysis:

- **`codebase`**: Scan workspace for source files and structure
- **`search`**: Full-text search across workspace files
- **`findTestFiles`**: Locate test sources and patterns
- **`runTests`**: Execute test suites for analysis
- **`editFiles`**: Create and modify documentation files
- **`runCommands`**: Execute shell commands for system analysis

## Examples

### Documentation Generation

```bash
orka chatmode architect \
  "Document the OrKa orchestration system focusing on agent lifecycle and workflow execution" \
  "Orchestrator,Agent,Node" \
  --artifact-type doc \
  --depth overview \
  --user-name "System Architect"
```

This generates comprehensive documentation covering:
- System overview and architecture
- Component interactions and data flows
- Error handling and reliability
- Security considerations
- Performance characteristics

### Diagram Generation

```bash
orka chatmode architect \
  "Show the sequence of operations in a typical workflow execution" \
  "Orchestrator,Agent,Memory" \
  --artifact-type diagram \
  --diagram-type sequence \
  --depth subsystem
```

This creates a sequence diagram showing:
- Actor interactions
- Message flows
- Processing steps
- Error conditions

### Gap Analysis

```bash
orka chatmode architect \
  "Identify gaps in our testing strategy for the memory system" \
  "MemorySystem,RedisBackend,VectorSearch" \
  --artifact-type gapscan \
  --depth overview
```

This produces a gap analysis report with:
- Current state assessment
- Identified deficiencies
- Prioritized recommendations
- Action plan with timelines

## Integration with OrKa Ecosystem

The ChatMode system seamlessly integrates with the broader OrKa ecosystem:

### Agent Registry
The `ArchitecturalDocumentationAgent` is registered in the agent registry and can be used in any OrKa workflow.

### Memory System
Generated documentation can be stored in OrKa's memory system for retrieval and reference in future workflows.

### CLI Integration
The ChatMode commands are fully integrated into the OrKa CLI with comprehensive help and error handling.

### Workflow Composition
ChatMode agents can be combined with other OrKa agents to create sophisticated documentation and analysis pipelines.

## Best Practices

### Effective Prompts
- Be specific about what aspects to document
- Include context about the system's purpose
- Specify the intended audience
- Mention any constraints or requirements

### Target Selection
- Use specific component names when possible
- Group related components logically
- Consider the scope of analysis needed

### Depth Selection
- Use `overview` for executive summaries
- Use `subsystem` for detailed technical documentation
- Use `interface-only` for API documentation

### Output Organization
- Maintain consistent naming conventions
- Organize outputs by project or system
- Version control generated documentation
- Regular cleanup of outdated artifacts

## Troubleshooting

### Common Issues

1. **Missing Required Parameters**
   - Ensure `prompt`, `targets`, and `artifactType` are provided
   - Check parameter spelling and case sensitivity

2. **Invalid Artifact Type**
   - Use only supported types: doc, diagram, testcases, gapscan, usecases
   - Check for typos in artifact type specification

3. **File Permission Issues**
   - Ensure write permissions to docs/ directory
   - Check available disk space
   - Verify directory structure exists

4. **Import Errors**
   - Ensure OrKa is properly installed with all dependencies
   - Check Python path and module resolution

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `'prompt' parameter is required` | Missing prompt | Provide a descriptive prompt |
| `Invalid artifact_type: xyz` | Unsupported type | Use doc, diagram, testcases, gapscan, or usecases |
| `Permission denied` | File system access | Check directory permissions |
| `Module not found` | Import issue | Reinstall OrKa with dependencies |

## Extension Points

The ChatMode system is designed for extensibility:

### Custom Artifact Types
Add new artifact types by extending the `HighLevelArchitectChatMode` class and implementing new generation methods.

### Additional Diagram Types
Support new diagram formats by adding methods to handle specific Mermaid diagram types.

### Custom Constraints
Extend the constraint system to support project-specific requirements and formatting preferences.

### Tool Integration
Add new analysis tools by implementing the tool interface and registering them with the ChatMode system.

_Generated with GitHub Copilot as directed by OrKa Development Team_