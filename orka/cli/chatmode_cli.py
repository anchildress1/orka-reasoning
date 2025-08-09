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
ChatMode CLI Interface
=====================

This module provides the CLI interface for ChatMode functionality.
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict

from orka.agents.architectural_documentation_agent import ArchitecturalDocumentationAgent

logger = logging.getLogger(__name__)


def setup_chatmode_command(subparsers) -> None:
    """Set up the chatmode command in the argument parser."""
    chatmode_parser = subparsers.add_parser(
        "chatmode", 
        help="Run specialized ChatMode workflows"
    )
    
    chatmode_subparsers = chatmode_parser.add_subparsers(dest="chatmode_command")
    
    # Architect command
    architect_parser = chatmode_subparsers.add_parser(
        "architect",
        help="Generate architectural documentation and diagrams"
    )
    architect_parser.add_argument("prompt", help="Description of what to document")
    architect_parser.add_argument("targets", help="Target components/systems to analyze")
    architect_parser.add_argument(
        "--artifact-type", 
        choices=["doc", "diagram", "testcases", "gapscan", "usecases"],
        default="doc",
        help="Type of artifact to generate"
    )
    architect_parser.add_argument(
        "--depth",
        choices=["overview", "subsystem", "interface-only"],
        default="overview",
        help="Level of detail to include"
    )
    architect_parser.add_argument(
        "--diagram-type",
        choices=["sequence", "flowchart", "class", "er", "state"],
        help="Type of diagram to generate (for diagram artifacts)"
    )
    architect_parser.add_argument(
        "--output-dir",
        default="docs",
        help="Output directory for generated files"
    )
    architect_parser.add_argument(
        "--format",
        choices=["markdown", "confluence"],
        default="markdown",
        help="Output format for documents"
    )
    architect_parser.add_argument(
        "--user-name",
        default="User",
        help="User name for generated footer"
    )
    architect_parser.add_argument(
        "--workspace",
        default=".",
        help="Workspace path for analysis"
    )
    architect_parser.set_defaults(func=handle_architect_command)


async def handle_architect_command(args) -> int:
    """Handle the architect command."""
    try:
        # Create agent
        agent = ArchitecturalDocumentationAgent(
            "architect-agent",
            workspace_path=args.workspace
        )
        
        await agent.initialize()
        
        # Prepare constraints
        constraints = {
            "format": args.format,
            "outputDir": args.output_dir
        }
        
        if args.diagram_type:
            constraints["diagram"] = args.diagram_type
        
        # Prepare context
        context = {
            "prompt": args.prompt,
            "targets": args.targets,
            "artifactType": args.artifact_type,
            "depth": args.depth,
            "constraints": constraints,
            "user_name": args.user_name
        }
        
        # Process request
        result = await agent.process(args.prompt, context)
        
        if result.get("success"):
            print("✅ Successfully generated architectural documentation!")
            
            artifact_result = result["result"]
            
            if "document" in artifact_result:
                print(f"📄 Document: {artifact_result['document']}")
            
            if "diagramFiles" in artifact_result and artifact_result["diagramFiles"]:
                print("📊 Diagrams:")
                for diagram in artifact_result["diagramFiles"]:
                    print(f"   - {diagram}")
            
            # Show summary if requested
            if hasattr(args, 'json') and args.json:
                print(json.dumps(result, indent=2))
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            return 1
            
        return 0
        
    except Exception as e:
        logger.error(f"Error in architect command: {str(e)}")
        print(f"❌ Error: {str(e)}")
        return 1


def run_chatmode_command(args) -> int:
    """Run a chatmode command asynchronously."""
    if hasattr(args, 'func') and args.func:
        # Check if the function is async
        if asyncio.iscoroutinefunction(args.func):
            return asyncio.run(args.func(args))
        else:
            return args.func(args)
    else:
        print("No command specified")
        return 1