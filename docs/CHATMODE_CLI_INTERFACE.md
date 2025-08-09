# ChatMode CLI Interface Demonstration

The ChatMode system adds a new `chatmode` command to the OrKa CLI with the following structure:

## Main Command Help
```
usage: orka [-h] [-v] [--json] {run,memory,chatmode} ...

OrKa - Orchestrator Kit for Agents

positional arguments:
  {run,memory,chatmode}
                        Available commands
    run                 Run orchestrator with configuration
    memory              Memory management commands
    chatmode            Run specialized ChatMode workflows

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbose logging
  --json                Output in JSON format
```

## ChatMode Command Help
```
usage: orka chatmode [-h] {architect} ...

positional arguments:
  {architect}  Available chatmodes
    architect  Generate architectural documentation and diagrams

optional arguments:
  -h, --help   show this help message and exit
```

## Architect Subcommand Help
```
usage: orka chatmode architect [-h] [--artifact-type {doc,diagram,testcases,gapscan,usecases}]
                               [--depth {overview,subsystem,interface-only}]
                               [--diagram-type {sequence,flowchart,class,er,state}]
                               [--output-dir OUTPUT_DIR] [--format {markdown,confluence}]
                               [--user-name USER_NAME] [--workspace WORKSPACE]
                               prompt targets

positional arguments:
  prompt                Description of what to document
  targets               Target components/systems to analyze

optional arguments:
  -h, --help            show this help message and exit
  --artifact-type {doc,diagram,testcases,gapscan,usecases}
                        Type of artifact to generate (default: doc)
  --depth {overview,subsystem,interface-only}
                        Level of detail to include (default: overview)
  --diagram-type {sequence,flowchart,class,er,state}
                        Type of diagram to generate (for diagram artifacts)
  --output-dir OUTPUT_DIR
                        Output directory for generated files (default: docs)
  --format {markdown,confluence}
                        Output format for documents (default: markdown)
  --user-name USER_NAME
                        User name for generated footer (default: User)
  --workspace WORKSPACE
                        Workspace path for analysis (default: .)
```

## Example Commands

### Generate Documentation
```bash
orka chatmode architect "Document the authentication system" "AuthService,UserManager" --artifact-type doc --depth overview
```

### Generate Sequence Diagram
```bash
orka chatmode architect "Show user login flow" "AuthService,Database" --artifact-type diagram --diagram-type sequence
```

### Generate Gap Analysis
```bash
orka chatmode architect "Analyze testing gaps" "TestSuite" --artifact-type gapscan --user-name "QA Lead"
```

## Full Integration Example

The ChatMode system is fully integrated into OrKa's architecture and can be used in several ways:

1. **Direct CLI usage** (shown above)
2. **Agent integration** in YAML workflows
3. **Programmatic usage** through the Python API

All methods produce the same high-quality architectural documentation following the ChatMode specification.

_Generated with GitHub Copilot as directed by OrKa Development Team_