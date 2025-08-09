# OrKa: Orchestrator Kit Agents
# Copyright © 2025 Marco Somma
#
# This file is part of OrKa – https://github.com/marcosomma/orka-reasoning
#
# Licensed under the Apache License, Version 2.0 (Apache 2.0).
# You may not use this file for commercial purposes without explicit permission.
#
# Full license: https://www.apache.org/licenses/LICENSE-2.0
# For commercial use, contact: marcosomma.work@gmail.com
#
# Required attribution: OrKa by Marco Somma – https://github.com/marcosomma/orka-reasoning

"""
ChatMode System for OrKa
========================

This module implements the ChatMode system for specialized AI workflows.
ChatModes are pre-configured workflows designed for specific use cases
like architectural documentation, gap analysis, and system design.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class ChatModeConfig:
    """Configuration for a specific ChatMode."""
    
    def __init__(self, 
                 name: str,
                 role: Dict[str, Any],
                 scope: Dict[str, Any],
                 inputs: Dict[str, Any],
                 outputs: Dict[str, Any],
                 constraints: Dict[str, Any],
                 behaviors: Dict[str, Any],
                 tools: List[str]):
        self.name = name
        self.role = role
        self.scope = scope
        self.inputs = inputs
        self.outputs = outputs
        self.constraints = constraints
        self.behaviors = behaviors
        self.tools = tools


class HighLevelArchitectChatMode:
    """
    High-Level Big Picture Architect ChatMode
    
    This ChatMode specializes in explaining and documenting software systems
    at a high level for fast onboarding, architectural clarity, and gap discovery.
    """
    
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.docs_folder = self.workspace_path / "docs"
        self.diagrams_folder = self.docs_folder / "diagrams"
        self.config = self._load_config()
        
    def _load_config(self) -> ChatModeConfig:
        """Load the configuration for this ChatMode."""
        return ChatModeConfig(
            name="high-level-big-picture-architect",
            role={
                "level": "PrincipalSystemsArchitect",
                "mission": "Explain and document software systems at a high level for fast onboarding, architectural clarity, and gap discovery."
            },
            scope={
                "focus": "Interfaces, contracts, data flows, major components, reliability behaviors, error surfaces, and integration points."
            },
            inputs={
                "prompt": {"required": True},
                "targets": {"required": True},
                "artifactType": {"required": True, "enum": ["doc", "diagram", "testcases", "gapscan", "usecases"]},
                "depth": {"required": False, "default": "overview", "enum": ["overview", "subsystem", "interface-only"]},
                "constraints": {"required": False}
            },
            outputs={
                "document": {"type": "markdownOrConfluence"},
                "diagramFiles": {"type": "mermaidFileRefs"}
            },
            constraints={
                "preferredDocsFolder": "docs/",
                "diagramFolder": "docs/diagrams/",
                "diagramDefaultMode": "file",
                "enforceDiagramEngine": "mermaid",
                "noOtherDiagramFormats": True,
                "defaultFormat": "markdown",
                "footerRequired": True,
                "footerTemplate": "_Generated with GitHub Copilot as directed by {USER_NAME_PLACEHOLDER}",
                "noGuessing": True,
                "iterationUntilComplete": True
            },
            behaviors={
                "askIfMissing": True,
                "highlightGaps": True
            },
            tools=[
                "codebase", "search", "findTestFiles", "runTests", 
                "editFiles", "runCommands"
            ]
        )
    
    def process(self, 
                prompt: str,
                targets: str,
                artifact_type: str,
                depth: str = "overview",
                constraints: Optional[Dict[str, Any]] = None,
                user_name: str = "User") -> Dict[str, Any]:
        """
        Process a request using the High-Level Architect ChatMode.
        
        Args:
            prompt: The main request/question
            targets: Target components/systems to analyze
            artifact_type: Type of artifact to generate (doc, diagram, testcases, gapscan, usecases)
            depth: Level of detail (overview, subsystem, interface-only)
            constraints: Additional constraints for the analysis
            user_name: Name of the user requesting the analysis
            
        Returns:
            Dict containing the generated documents and diagrams
        """
        logger.info(f"Processing {artifact_type} request: {prompt}")
        
        # Validate inputs
        if artifact_type not in ["doc", "diagram", "testcases", "gapscan", "usecases"]:
            raise ValueError(f"Invalid artifact_type: {artifact_type}")
            
        if depth not in ["overview", "subsystem", "interface-only"]:
            raise ValueError(f"Invalid depth: {depth}")
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Process based on artifact type
        if artifact_type == "doc":
            return self._generate_documentation(prompt, targets, depth, constraints, user_name)
        elif artifact_type == "diagram":
            return self._generate_diagram(prompt, targets, depth, constraints, user_name)
        elif artifact_type == "testcases":
            return self._generate_testcases(prompt, targets, depth, constraints, user_name)
        elif artifact_type == "gapscan":
            return self._generate_gapscan(prompt, targets, depth, constraints, user_name)
        elif artifact_type == "usecases":
            return self._generate_usecases(prompt, targets, depth, constraints, user_name)
        else:
            raise ValueError(f"Unsupported artifact_type: {artifact_type}")
    
    def _ensure_directories(self) -> None:
        """Ensure required directories exist."""
        self.docs_folder.mkdir(exist_ok=True)
        self.diagrams_folder.mkdir(exist_ok=True)
    
    def _scan_codebase(self, targets: str) -> Dict[str, Any]:
        """Scan the codebase for the specified targets."""
        # This would integrate with the actual codebase scanning logic
        # For now, return a placeholder structure
        return {
            "files_found": [],
            "components": [],
            "interfaces": [],
            "dependencies": []
        }
    
    def _generate_footer(self, user_name: str) -> str:
        """Generate the required footer."""
        return f"_Generated with GitHub Copilot as directed by {user_name}_"
    
    def _generate_documentation(self, prompt: str, targets: str, depth: str, 
                              constraints: Optional[Dict[str, Any]], user_name: str) -> Dict[str, Any]:
        """Generate documentation artifact."""
        # Scan codebase
        scan_result = self._scan_codebase(targets)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"architecture_doc_{timestamp}.md"
        filepath = self.docs_folder / filename
        
        # Generate content
        content = self._create_documentation_content(prompt, targets, depth, scan_result, user_name)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Generate accompanying diagram
        diagram_result = self._generate_flowchart_diagram(prompt, targets, depth, constraints, user_name)
        
        return {
            "document": str(filepath),
            "diagramFiles": [diagram_result["diagram_file"]] if diagram_result else [],
            "content": content
        }
    
    def _generate_diagram(self, prompt: str, targets: str, depth: str,
                         constraints: Optional[Dict[str, Any]], user_name: str) -> Dict[str, Any]:
        """Generate diagram artifact."""
        diagram_type = "flowchart"
        if constraints and "diagram" in constraints:
            diagram_type = constraints["diagram"]
        
        if diagram_type == "sequence":
            return self._generate_sequence_diagram(prompt, targets, depth, constraints, user_name)
        elif diagram_type == "flowchart":
            return self._generate_flowchart_diagram(prompt, targets, depth, constraints, user_name)
        elif diagram_type == "class":
            return self._generate_class_diagram(prompt, targets, depth, constraints, user_name)
        elif diagram_type == "er":
            return self._generate_er_diagram(prompt, targets, depth, constraints, user_name)
        elif diagram_type == "state":
            return self._generate_state_diagram(prompt, targets, depth, constraints, user_name)
        else:
            return self._generate_flowchart_diagram(prompt, targets, depth, constraints, user_name)
    
    def _generate_flowchart_diagram(self, prompt: str, targets: str, depth: str,
                                   constraints: Optional[Dict[str, Any]], user_name: str) -> Dict[str, Any]:
        """Generate a mermaid flowchart diagram."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"flowchart_{timestamp}.mmd"
        filepath = self.diagrams_folder / filename
        
        # Generate mermaid content
        mermaid_content = self._create_flowchart_content(prompt, targets, depth)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(mermaid_content)
        
        return {
            "diagram_file": str(filepath),
            "diagram_type": "flowchart",
            "content": mermaid_content
        }
    
    def _generate_sequence_diagram(self, prompt: str, targets: str, depth: str,
                                 constraints: Optional[Dict[str, Any]], user_name: str) -> Dict[str, Any]:
        """Generate a mermaid sequence diagram."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sequence_{timestamp}.mmd"
        filepath = self.diagrams_folder / filename
        
        mermaid_content = f"""sequenceDiagram
    participant User
    participant System
    participant {targets}
    
    User->>System: {prompt}
    System->>{targets}: Process Request
    {targets}->>System: Return Result
    System->>User: Provide Response
    
    Note over User,{targets}: {self._generate_footer(user_name)}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(mermaid_content)
        
        return {
            "diagram_file": str(filepath),
            "diagram_type": "sequence",
            "content": mermaid_content
        }
    
    def _generate_class_diagram(self, prompt: str, targets: str, depth: str,
                              constraints: Optional[Dict[str, Any]], user_name: str) -> Dict[str, Any]:
        """Generate a mermaid class diagram."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"class_{timestamp}.mmd"
        filepath = self.diagrams_folder / filename
        
        mermaid_content = f"""classDiagram
    class {targets} {{
        +attributes
        +methods()
    }}
    
    class Component {{
        +process()
        +validate()
    }}
    
    {targets} --> Component : uses
    
    note "{self._generate_footer(user_name)}"
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(mermaid_content)
        
        return {
            "diagram_file": str(filepath),
            "diagram_type": "class",
            "content": mermaid_content
        }
    
    def _generate_er_diagram(self, prompt: str, targets: str, depth: str,
                           constraints: Optional[Dict[str, Any]], user_name: str) -> Dict[str, Any]:
        """Generate a mermaid entity-relationship diagram."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"er_{timestamp}.mmd"
        filepath = self.diagrams_folder / filename
        
        mermaid_content = f"""erDiagram
    Entity1 ||--o{{ Entity2 : relationship
    Entity1 {{
        string id PK
        string name
    }}
    Entity2 {{
        string id PK
        string entity1_id FK
        string data
    }}
    
    note "{self._generate_footer(user_name)}"
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(mermaid_content)
        
        return {
            "diagram_file": str(filepath),
            "diagram_type": "er",
            "content": mermaid_content
        }
    
    def _generate_state_diagram(self, prompt: str, targets: str, depth: str,
                              constraints: Optional[Dict[str, Any]], user_name: str) -> Dict[str, Any]:
        """Generate a mermaid state diagram."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"state_{timestamp}.mmd"
        filepath = self.diagrams_folder / filename
        
        mermaid_content = f"""stateDiagram-v2
    [*] --> Initial
    Initial --> Processing : {prompt}
    Processing --> Complete : Success
    Processing --> Error : Failure
    Error --> Processing : Retry
    Complete --> [*]
    
    note "{self._generate_footer(user_name)}"
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(mermaid_content)
        
        return {
            "diagram_file": str(filepath),
            "diagram_type": "state",
            "content": mermaid_content
        }
    
    def _generate_testcases(self, prompt: str, targets: str, depth: str,
                          constraints: Optional[Dict[str, Any]], user_name: str) -> Dict[str, Any]:
        """Generate test cases artifact."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"testcases_{timestamp}.md"
        filepath = self.docs_folder / filename
        
        content = f"""# Test Cases for {targets}

## Overview
Test cases generated for: {prompt}

## Test Categories

### 1. Unit Tests
- Component functionality tests
- Input validation tests
- Error handling tests

### 2. Integration Tests
- System integration tests
- API endpoint tests
- Data flow tests

### 3. Performance Tests
- Load testing
- Stress testing
- Scalability testing

## Test Cases

### TC001 - Basic Functionality
**Objective**: Verify basic functionality of {targets}
**Prerequisites**: System is running
**Steps**:
1. Initialize {targets}
2. Execute primary function
3. Verify expected output

**Expected Result**: System responds correctly

### TC002 - Error Handling
**Objective**: Verify error handling in {targets}
**Prerequisites**: System is running
**Steps**:
1. Provide invalid input
2. Observe system response
3. Verify error message

**Expected Result**: Appropriate error message displayed

{self._generate_footer(user_name)}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "document": str(filepath),
            "diagramFiles": [],
            "content": content
        }
    
    def _generate_gapscan(self, prompt: str, targets: str, depth: str,
                        constraints: Optional[Dict[str, Any]], user_name: str) -> Dict[str, Any]:
        """Generate gap scan artifact."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gapscan_{timestamp}.md"
        filepath = self.docs_folder / filename
        
        content = f"""# Gap Analysis for {targets}

## Executive Summary
Gap analysis conducted for: {prompt}

## Current State Assessment

### Strengths
- Existing functionality
- Working components
- Established patterns

### Identified Gaps

#### 1. Documentation Gaps
- Missing API documentation
- Incomplete user guides
- Outdated technical specifications

#### 2. Testing Gaps
- Insufficient test coverage
- Missing integration tests
- No performance benchmarks

#### 3. Architecture Gaps
- Unclear component boundaries
- Missing error handling
- Scalability concerns

#### 4. Security Gaps
- Authentication mechanisms
- Authorization controls
- Data protection measures

## Recommendations

### High Priority
1. Implement comprehensive testing strategy
2. Create detailed API documentation
3. Establish error handling patterns

### Medium Priority
1. Improve component architecture
2. Add security measures
3. Performance optimization

### Low Priority
1. Code refactoring
2. Documentation updates
3. Tool improvements

## Action Plan

| Priority | Action Item | Timeline | Owner |
|----------|-------------|----------|-------|
| High | Testing Strategy | 2 weeks | TBD |
| High | API Documentation | 1 week | TBD |
| Medium | Security Review | 4 weeks | TBD |

{self._generate_footer(user_name)}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "document": str(filepath),
            "diagramFiles": [],
            "content": content
        }
    
    def _generate_usecases(self, prompt: str, targets: str, depth: str,
                         constraints: Optional[Dict[str, Any]], user_name: str) -> Dict[str, Any]:
        """Generate use cases artifact."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"usecases_{timestamp}.md"
        filepath = self.docs_folder / filename
        
        content = f"""# Use Cases for {targets}

## Overview
Use cases defined for: {prompt}

## Actors
- Primary User
- System Administrator
- External System

## Use Cases

### UC001 - Primary User Interaction
**Actor**: Primary User
**Goal**: {prompt}
**Preconditions**: User is authenticated
**Main Flow**:
1. User accesses {targets}
2. System presents interface
3. User provides input
4. System processes request
5. System returns result

**Alternative Flows**:
- 4a. Invalid input provided
  - 4a1. System displays error message
  - 4a2. Return to step 3

**Postconditions**: Request is processed successfully

### UC002 - System Administration
**Actor**: System Administrator
**Goal**: Manage {targets} configuration
**Preconditions**: Administrator has access
**Main Flow**:
1. Administrator accesses admin interface
2. System displays configuration options
3. Administrator modifies settings
4. System validates changes
5. System applies configuration

**Alternative Flows**:
- 4a. Invalid configuration
  - 4a1. System rejects changes
  - 4a2. Return to step 3

**Postconditions**: System is configured correctly

### UC003 - External System Integration
**Actor**: External System
**Goal**: Integrate with {targets}
**Preconditions**: API credentials configured
**Main Flow**:
1. External system sends request
2. System validates credentials
3. System processes request
4. System returns response

**Alternative Flows**:
- 2a. Invalid credentials
  - 2a1. System returns authentication error
  - 2a2. End use case

**Postconditions**: Integration is successful

{self._generate_footer(user_name)}
"""
        
        # Generate sequence diagram for use cases
        diagram_result = self._generate_sequence_diagram(prompt, targets, depth, constraints, user_name)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "document": str(filepath),
            "diagramFiles": [diagram_result["diagram_file"]],
            "content": content
        }
    
    def _create_documentation_content(self, prompt: str, targets: str, depth: str,
                                    scan_result: Dict[str, Any], user_name: str) -> str:
        """Create the main documentation content."""
        return f"""# Architecture Documentation for {targets}

## Executive Summary
This document provides {depth} level documentation for: {prompt}

## System Overview

### Purpose
The {targets} system is designed to handle the following requirements:
- {prompt}

### Architecture Principles
- Modularity and separation of concerns
- Scalability and performance
- Reliability and error handling
- Security and data protection

## Components

### Core Components
- **Main Processing Unit**: Handles primary business logic
- **Data Layer**: Manages data persistence and retrieval
- **API Layer**: Provides external interfaces
- **Configuration Management**: Handles system configuration

### Component Interactions
Components interact through well-defined interfaces and contracts.

## Data Flow

### Primary Data Flow
1. Input validation and preprocessing
2. Business logic processing
3. Data persistence
4. Response generation

### Error Handling
- Input validation errors
- Processing exceptions
- Data consistency checks
- System recovery procedures

## Integration Points

### External Dependencies
- External APIs and services
- Database systems
- Configuration sources
- Monitoring and logging systems

### Internal Interfaces
- Component-to-component communication
- Event handling mechanisms
- Data transformation layers

## Reliability Behaviors

### Error Surfaces
- Input validation failures
- External service timeouts
- Resource exhaustion
- Configuration errors

### Recovery Mechanisms
- Graceful degradation
- Retry policies
- Circuit breaker patterns
- Fallback procedures

## Security Considerations

### Authentication
- User authentication mechanisms
- Service-to-service authentication
- Token management

### Authorization
- Role-based access control
- Resource-level permissions
- API access controls

### Data Protection
- Data encryption at rest
- Data encryption in transit
- PII handling procedures

## Performance Characteristics

### Scalability
- Horizontal scaling capabilities
- Vertical scaling considerations
- Resource utilization patterns

### Monitoring
- Key performance indicators
- Alerting mechanisms
- Logging strategies

## Future Considerations

### Planned Enhancements
- Feature roadmap items
- Technical debt reduction
- Performance optimizations

### Migration Strategies
- Version upgrade procedures
- Data migration approaches
- Backward compatibility

{self._generate_footer(user_name)}
"""
    
    def _create_flowchart_content(self, prompt: str, targets: str, depth: str) -> str:
        """Create mermaid flowchart content."""
        return f"""flowchart TD
    A[Start: {prompt}] --> B[Initialize {targets}]
    B --> C[Process Input]
    C --> D{{Validate Input}}
    D -->|Valid| E[Execute Business Logic]
    D -->|Invalid| F[Return Error]
    E --> G[Process Data]
    G --> H[Generate Response]
    H --> I[End: Success]
    F --> J[End: Error]
    
    subgraph "Core Processing"
        E
        G
    end
    
    subgraph "Error Handling"
        F
        J
    end
    
    style A fill:#e1f5fe
    style I fill:#c8e6c9
    style J fill:#ffcdd2
"""