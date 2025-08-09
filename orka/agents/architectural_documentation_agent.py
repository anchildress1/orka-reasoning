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
Architectural Documentation Agent
===============================

This agent implements the ChatMode functionality for generating architectural
documentation and diagrams.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import the base class locally to avoid dependency issues during development
try:
    from orka.agents.base_agent import BaseAgent
except ImportError:
    # Create a minimal base class for testing
    class BaseAgent:
        def __init__(self, agent_id: str, **kwargs):
            self.agent_id = agent_id
            
        async def initialize(self) -> None:
            pass

from orka.cli.chatmode import HighLevelArchitectChatMode

logger = logging.getLogger(__name__)


class ArchitecturalDocumentationAgent(BaseAgent):
    """
    Agent for generating architectural documentation and diagrams.
    
    This agent implements the high-level-big-picture-architect ChatMode
    for creating comprehensive system documentation.
    """
    
    def __init__(self, agent_id: str, **kwargs):
        super().__init__(agent_id, **kwargs)
        self.chatmode = None
        self.workspace_path = kwargs.get('workspace_path', '.')
        
    async def initialize(self) -> None:
        """Initialize the architectural documentation agent."""
        await super().initialize()
        self.chatmode = HighLevelArchitectChatMode(self.workspace_path)
        logger.info(f"Initialized ArchitecturalDocumentationAgent: {self.agent_id}")
    
    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a request for architectural documentation.
        
        Args:
            input_data: The input request (can be a prompt or structured data)
            context: Additional context including chatmode parameters
            
        Returns:
            Dict containing generated documents and diagrams
        """
        try:
            # Parse input parameters
            params = self._parse_input(input_data, context)
            
            # Validate required parameters
            if not params.get('prompt'):
                raise ValueError("'prompt' parameter is required")
            if not params.get('targets'):
                raise ValueError("'targets' parameter is required")
            if not params.get('artifactType'):
                raise ValueError("'artifactType' parameter is required")
                
            # Process using ChatMode
            result = self.chatmode.process(
                prompt=params['prompt'],
                targets=params['targets'],
                artifact_type=params['artifactType'],
                depth=params.get('depth', 'overview'),
                constraints=params.get('constraints'),
                user_name=params.get('user_name', 'User')
            )
            
            logger.info(f"Generated {params['artifactType']} for {params['targets']}")
            
            return {
                'success': True,
                'result': result,
                'metadata': {
                    'agent_id': self.agent_id,
                    'artifact_type': params['artifactType'],
                    'targets': params['targets'],
                    'depth': params.get('depth', 'overview')
                }
            }
            
        except Exception as e:
            logger.error(f"Error in ArchitecturalDocumentationAgent: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'metadata': {
                    'agent_id': self.agent_id
                }
            }
    
    def _parse_input(self, input_data: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parse input data and context to extract parameters.
        
        Args:
            input_data: The main input string
            context: Additional context parameters
            
        Returns:
            Dict of parsed parameters
        """
        params = {}
        
        # If context contains parameters, use them
        if context:
            params.update(context)
        
        # If input_data appears to be structured (contains =), parse it
        if '=' in input_data:
            for line in input_data.split('\n'):
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    params[key.strip()] = value.strip()
        else:
            # Treat input_data as the prompt if no prompt is already set
            if 'prompt' not in params:
                params['prompt'] = input_data
        
        return params
    
    def get_supported_artifact_types(self) -> List[str]:
        """Get list of supported artifact types."""
        return ["doc", "diagram", "testcases", "gapscan", "usecases"]
    
    def get_supported_depths(self) -> List[str]:
        """Get list of supported depth levels."""
        return ["overview", "subsystem", "interface-only"]
    
    def get_supported_diagram_types(self) -> List[str]:
        """Get list of supported diagram types."""
        return ["sequence", "flowchart", "class", "er", "state"]


# Factory function for agent registration
def create_architectural_documentation_agent(agent_id: str, **kwargs) -> ArchitecturalDocumentationAgent:
    """Factory function to create an ArchitecturalDocumentationAgent."""
    return ArchitecturalDocumentationAgent(agent_id, **kwargs)