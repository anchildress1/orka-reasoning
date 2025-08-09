"""
Test for the ArchitecturalDocumentationAgent and ChatMode system.
"""

import asyncio
import tempfile
from pathlib import Path

import pytest

from orka.agents.architectural_documentation_agent import ArchitecturalDocumentationAgent
from orka.cli.chatmode import HighLevelArchitectChatMode


@pytest.mark.asyncio
async def test_architectural_documentation_agent():
    """Test the ArchitecturalDocumentationAgent."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create agent
        agent = ArchitecturalDocumentationAgent(
            "test-agent",
            workspace_path=temp_dir
        )
        
        await agent.initialize()
        
        # Test context with required parameters
        context = {
            "prompt": "Document the authentication system",
            "targets": "AuthService",
            "artifactType": "doc",
            "depth": "overview",
            "user_name": "TestUser"
        }
        
        # Process request
        result = await agent.process("Test input", context)
        
        # Check result
        assert result["success"] is True
        assert "result" in result
        assert "document" in result["result"]
        
        # Check that file was created
        doc_path = Path(result["result"]["document"])
        assert doc_path.exists()
        assert doc_path.suffix == ".md"


def test_chatmode_config():
    """Test ChatMode configuration."""
    chatmode = HighLevelArchitectChatMode()
    config = chatmode.config
    
    assert config.name == "high-level-big-picture-architect"
    assert config.role["level"] == "PrincipalSystemsArchitect"
    assert "prompt" in config.inputs
    assert "targets" in config.inputs
    assert "artifactType" in config.inputs
    assert config.constraints["enforceDiagramEngine"] == "mermaid"


def test_chatmode_artifact_types():
    """Test all artifact types."""
    with tempfile.TemporaryDirectory() as temp_dir:
        chatmode = HighLevelArchitectChatMode(temp_dir)
        
        artifact_types = ["doc", "diagram", "testcases", "gapscan", "usecases"]
        
        for artifact_type in artifact_types:
            result = chatmode.process(
                prompt="Test prompt",
                targets="TestComponent",
                artifact_type=artifact_type,
                user_name="TestUser"
            )
            
            assert "document" in result or "diagram_file" in result
            
            # Check that files were created
            if "document" in result:
                doc_path = Path(result["document"])
                assert doc_path.exists()
            
            if "diagramFiles" in result and result["diagramFiles"]:
                for diagram_file in result["diagramFiles"]:
                    diagram_path = Path(diagram_file)
                    assert diagram_path.exists()


def test_diagram_types():
    """Test all diagram types."""
    with tempfile.TemporaryDirectory() as temp_dir:
        chatmode = HighLevelArchitectChatMode(temp_dir)
        
        diagram_types = ["sequence", "flowchart", "class", "er", "state"]
        
        for diagram_type in diagram_types:
            result = chatmode.process(
                prompt="Test prompt",
                targets="TestComponent", 
                artifact_type="diagram",
                constraints={"diagram": diagram_type},
                user_name="TestUser"
            )
            
            assert "diagram_file" in result
            diagram_path = Path(result["diagram_file"])
            assert diagram_path.exists()
            assert result["diagram_type"] == diagram_type


@pytest.mark.asyncio
async def test_agent_error_handling():
    """Test agent error handling."""
    with tempfile.TemporaryDirectory() as temp_dir:
        agent = ArchitecturalDocumentationAgent(
            "test-agent",
            workspace_path=temp_dir
        )
        
        await agent.initialize()
        
        # Test missing required parameter
        context = {
            "prompt": "Test prompt"
            # Missing targets and artifactType
        }
        
        result = await agent.process("Test input", context)
        
        assert result["success"] is False
        assert "error" in result


if __name__ == "__main__":
    # Run basic test
    asyncio.run(test_architectural_documentation_agent())
    print("✅ Basic test passed!")