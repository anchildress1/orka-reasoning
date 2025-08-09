# ChatMode Usage Examples

This document demonstrates how to use the newly implemented ChatMode system for architectural documentation.

## CLI Usage Examples

### Generate Documentation
```bash
# Generate comprehensive documentation
orka chatmode architect \
  "Document the OrKa orchestration system focusing on agent lifecycle and workflow execution" \
  "Orchestrator,Agent,Node,Memory" \
  --artifact-type doc \
  --depth overview \
  --user-name "System Architect"
```

### Generate Diagrams
```bash
# Generate sequence diagram
orka chatmode architect \
  "Show the sequence of operations in a typical workflow execution" \
  "Orchestrator,Agent,Memory" \
  --artifact-type diagram \
  --diagram-type sequence \
  --depth subsystem

# Generate flowchart
orka chatmode architect \
  "Create a flowchart showing the data flow in the memory system" \
  "MemoryManager,RedisBackend,VectorSearch" \
  --artifact-type diagram \
  --diagram-type flowchart
```

### Generate Specialized Artifacts
```bash
# Generate gap analysis
orka chatmode architect \
  "Identify gaps in our testing strategy for the memory system" \
  "MemorySystem,RedisBackend,VectorSearch" \
  --artifact-type gapscan \
  --depth overview

# Generate test cases
orka chatmode architect \
  "Create test cases for the authentication system" \
  "AuthService,UserManager,TokenHandler" \
  --artifact-type testcases

# Generate use cases
orka chatmode architect \
  "Document user workflows for the ChatMode system" \
  "CLI,ChatMode,FileSystem" \
  --artifact-type usecases
```

## Generated Output

The ChatMode system automatically creates organized documentation:

```
docs/
├── architecture_doc_20250809_071134.md
├── gapscan_20250809_071145.md
├── testcases_20250809_071156.md
├── usecases_20250809_071207.md
└── diagrams/
    ├── sequence_20250809_071134.mmd
    ├── flowchart_20250809_071145.mmd
    ├── class_20250809_071156.mmd
    └── state_20250809_071207.mmd
```

## Key Features Demonstrated

✅ **Multiple Artifact Types**: Documentation, diagrams, test cases, gap analysis, use cases
✅ **Multiple Diagram Types**: Sequence, flowchart, class, ER, state diagrams  
✅ **Proper Organization**: Automatic file organization in docs/ and docs/diagrams/
✅ **Mermaid Format**: All diagrams in standard mermaid format
✅ **User Attribution**: Footer with user name in all generated content
✅ **Timestamp Naming**: Unique filenames with timestamp for traceability

## Integration with OrKa Workflows

The ChatMode system integrates seamlessly with OrKa workflows via the `architectural-documentation` agent type.

_Generated with GitHub Copilot as directed by OrKa Development Team_